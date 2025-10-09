from app.schema.common import WillSmith


class ResultsService:
    async def get_results(self, questionnaire_id: int, session_id: int):
        return WillSmith(img_url="https://a.pinatafarm.com/540x494/76636b7956/tada-will-smith.jpg")
