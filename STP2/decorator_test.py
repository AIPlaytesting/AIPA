
def deco(func):
    def extened():
        ctx = ""
        return raw(ctx)
    return extened

@deco
def raw(ctx):
    print(ctx)

raw()