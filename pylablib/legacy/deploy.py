if __name__=="__main__":
    from builtins import input
    import os
    from .core.utils import versioning #@UnresolvedImport

    os.chdir("../")
    name=input("Choose storage label (default is empty): ")
    versioning.store("snapshots",label=name or None)
    input("Done")