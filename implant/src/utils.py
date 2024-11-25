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


def choose_target(res, method="GET"):
    print(res)
    return "/"
