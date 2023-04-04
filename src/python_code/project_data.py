from pathlib import Path


class ProjectData:
    @staticmethod
    def project_path() -> Path:
        return Path(__file__).parents[2]

    @staticmethod
    def data_path() -> Path:
        return ProjectData.project_path().joinpath("data/data.json")
