import re
import random


"""
Check if the server IP is an IPv4 with or without port specification.
Port specification is not assessed.
@param: server: IPv4 string (i.e. 0.0.0.0, 127.0.0.1:5000, 8.8.8.8:45000)
@returns: True if server is an IPv4, False either
"""
def is_ipv4(server):
    if ":" in server:
        splitted = server.split(":")
        ip = splitted[0]
        port = splitted[1]
    else:
        ip = server
        port = "80"
    parts = ip.split(".")
    if len(parts) < 4:
        return False
    for i in range(4):
        try:
            if not int(parts[i]) >= 0 or not int(parts[i]) < 256:
                return False
        except ValueError:
            return False
    return True


"""
This function choose randomly an URI available in res with the good method
This function uses the config file to know which URI relies to which method
@param: res: the HTML page received (string)
@param: method: GET or POST, HTTP method
@returns: string: the URI chosen
"""
def choose_target(res, configs, method="GET"):
    try:
        urls = configs.get("get_dictionary") if method == "GET" else configs.get("post_dictionary")
        available = ["/"]
        for url in urls:
            if url+'"' in res:
                available.append(url)
        print(available)
        # TODO choose target in URI available in argument res
        return random.choice(available)
    except:
        return "/forum"
