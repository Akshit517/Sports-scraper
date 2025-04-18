import pathway as pw


class CommentarySchema(pw.Schema):
    Ball: str
    Commentary: str


class CommentaryHandler:
    @staticmethod
    def read_input(code: str):
        commentary_table = pw.io.csv.read(
            f"../{code}.csv",
            schema=CommentarySchema,
            mode="streaming",  # Use 'static' if not simulating streaming
        )

        formatted = commentary_table.select(
            entry_id=pw.this.Ball,
            content=pw.this.Commentary,
        )
        return formatted
