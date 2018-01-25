from zipfile import ZipFile
import glob
import sys
import os


def build_installer():
    sys.path.append("src")
    import __plugin__

    path_prefix = "PythonPlugIns/{0.title} {0.id}/dev/".format(__plugin__)
    files = glob.glob("src/*.py")

    macrhi = ZipFile("{}.macrhi".format(__plugin__.title), "w")
    rhi = ZipFile("{}.rhi".format(__plugin__.title), "w")

    for f in files:
        archive_path_rhi = os.path.relpath(f, "src/")
        archive_path_macrhi = os.path.join(path_prefix + archive_path_rhi)

        rhi.write(f, archive_path_rhi)
        macrhi.write(f, archive_path_macrhi)

    macrhi.close()
    rhi.close()


if __name__ == "__main__":
    build_installer()
