import pandas as pd


def parse(filename):
    f = open(filename)
    lines = []
    for l in f.readlines():
        if l.startswith(" ") or l.startswith("\t"):
            lines[-1] = lines[-1] + "\n" + l.strip()
        elif l.strip().startswith("#") or l.strip() == "":
            pass
        else:
            lines.append(l)

  
    objects = {}
    schema = {}
    last_key = None
    last_table = None

    for l in lines:
        arr = l.split()
        table_attr = arr[0] 
        oid = arr[1]
        value = " ".join(arr[2:])

        if table_attr.endswith(":"):
            print("SIngle line schema ver" + table_attr+ ".. " +  str(schema ))
            # this is the single row version, we must have defined a special 
            # schema table thing

            if table_attr not in schema:
                print("define schema")
                schema[table_attr] = arr[1:]
                if table_attr[:-1] not in objects:
                    objects[table_attr[:-1]] = {}
            else:
                print("FFFFFFFFFFFFFFFFFF")
                rc = len(schema[table_attr])
                d = {}
                row = arr[1:]
                for i in range(rc):
                    d[schema[table_attr][i]] = row[i]
                print(d) 
                d[schema[table_attr][i]] = d[schema[table_attr][i]] + " ".join(row[rc:])
                objects[table_attr[:-1]][d['key']] = d
                 
        else:
          
            if "." in table_attr:
                arr = table_attr.split(".")
                table = arr[0]
                attr = ".".join(arr[1:])
            else:
                table = table_attr
                attr = "value"

            if table not in objects:
                objects[table] = {}

            if oid not in objects[table]:
                objects[table][oid] = {}
                objects[table][oid]['key'] = oid

            objects[table][oid][attr] = value

    #print(objects)
    dfs = {}
    for t in objects:
        print(objects[t])
        dfs[t] = pd.DataFrame(objects[t]).transpose()

    return dfs


if __name__ == "__main__":
    import sys
    print(parse(sys.argv[1]))
