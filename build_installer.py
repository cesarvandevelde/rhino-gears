from zipfile import ZipFile
import glob
import sys
import os


def build_installer():
    sys.path.append("src")
    import __plugin__

    path_prefix = "PythonPlugIns/{0.title} {0.id}/dev/".format(__plugin__)
    files = glob.glob("src/*.py")

    # TODO: Generate .rhi installer for Windows
    with ZipFile("{}.macrhi".format(__plugin__.title), "w") as archive:
        for f in files:
            archive_path = os.path.relpath(f, "src/")
            archive_path = os.path.join(path_prefix + archive_path)

            archive.write(f, archive_path)


if __name__ == "__main__":
    build_installer()
