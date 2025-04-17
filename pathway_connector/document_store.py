import pathway as pw


class InputSchema(pw.Schema):
    value: int


input_table = pw.io.csv.read('../../', schema=InputSchema)
