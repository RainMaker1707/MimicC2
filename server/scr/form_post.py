from flask import render_template


print(render_template("form.html", 
                    CONTENT=render_template("form_input.html", 
                                            LABEL="Pseudo",
                                            TYPE="text",
                                            )
                    )
    )