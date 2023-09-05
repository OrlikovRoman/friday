from tokens.token import type_list
from tokens.token import no_lex_type_list
from tokens.token import Token
import re
from utils import console


class Lexer:
    def analysis(self, command):
        self.command = command
        self.position = 0
        self.token_list: list = []

        self.string: bool = False
        self.string_token: Token = None
        while self.parse():
            ...

        self.token_list = list(
            filter(
                lambda x: x.type.name != type_list.get("space").name,
                self.token_list
            )
        )

        return self.token_list

    def create_string(self):
        if self.string_token != None:
            self.string_token.text = self.string_token.text.strip(
                " ")
            self.token_list.append(self.string_token)

        self.string_token = None
        self.string = False

    def parse(self):
        if len(self.command) < self.position:
            return False

        for token_type in type_list.values():
            command = self.command[self.position:]
            for regex in token_type.regex:
                result = re.match(r"^%s" % regex, command)

                if result and result[0]:
                    self.position += len(result[0])

                    if token_type.name == "end":
                        if self.string == False:
                            token_type = type_list.get("string")
                        else:
                            self.create_string()

                    if self.string == False:
                        token: Token = Token(
                            token_type, result[0], self.position
                        )
                        self.token_list.append(token)
                        if token_type.is_owner_string:
                            self.string = True
                            self.string_token = Token(
                                type_list.get(
                                    "string"), "", self.position
                            )
                    else:
                        self.string_token.text += str(result[0])
                        self.string_token.position = self.position

                    return True

        self.create_string()
        return False
