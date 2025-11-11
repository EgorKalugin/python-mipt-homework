from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import ast
import operator

app = FastAPI()

expression_cache: str | None = None
arguments_cache: dict[str, float] | None = None


@app.get("/sum")
async def sum(a: float, b: float) -> float:
    return a + b


@app.get("/subtract")
async def subtract(a: float, b: float) -> float:
    return a - b


@app.get("/multiply")
async def multiply(a: float, b: float) -> float:
    return a * b


@app.get("/divide")
async def divide(a: float, b: float) -> float:
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return a / b


@app.get("/expression")
async def get_expression() -> dict | str:
    if expression_cache is None:
        return "No expression set."
    return {"expression": expression_cache, "arguments": arguments_cache or {}}


@app.post("/arguments")
async def set_arguments_dict(args: dict[str, float]) -> str:
    global arguments_cache
    arguments_cache = args
    return "Arguments set."


@app.post("/argument")
async def set_argument(argument: str, value: float) -> str:
    global arguments_cache
    if arguments_cache is None:
        arguments_cache = {}
    arguments_cache[argument] = value
    return "Argument set."


@app.delete("/argument")
async def delete_argument(argument: str) -> str:
    global arguments_cache
    if arguments_cache is None or argument not in arguments_cache:
        raise HTTPException(status_code=400, detail="Argument key not found.")
    del arguments_cache[argument]
    return "Argument deleted."


@app.delete("/arguments")
async def clear_arguments() -> str:
    global arguments_cache
    arguments_cache = None
    return "All arguments cleared."


@app.post("/expression")
async def set_expression(expr: str) -> str:
    global expression_cache
    expression_cache = expr
    return "Expression set."


@app.get("/arguments")
async def get_arguments() -> dict[str, float]:
    return arguments_cache or {}

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def eval_expr(expr: str, variables: dict[str, float]) :
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](_eval(node.operand))
        elif isinstance(node, ast.Name):
            return variables[node.id]
        else:
            raise TypeError(f"Unsupported node type: {type(node)}")

    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)

@app.get("/evaluate")
async def evaluate_expression() -> float:
    if expression_cache is None:
        raise HTTPException(status_code=400, detail="No expression set.")

    try:
        return float(eval_expr(expression_cache, arguments_cache or {}))
    except BaseException as e:
        raise HTTPException(
            status_code=400, detail=f"Error evaluating expression: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
