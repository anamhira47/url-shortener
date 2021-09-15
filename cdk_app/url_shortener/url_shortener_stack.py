from aws_cdk import core
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway

class UrlShortenerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = aws_dynamodb.Table(self, "mapping-table",
                                   partition_key=aws_dynamodb.Attribute(
                                       name="id",
                                       type=aws_dynamodb.AttributeType.STRING))
        handler = aws_lambda.Function(self, "backend",
                                        runtime=aws_lambda.Runtime.PYTHON_3_7,
                                        handler="handler.main",
                                        code=aws_lambda.AssetCode(path="./lambda"))
        
        table.grant_read_write_data(handler)
        handler.add_environment('TABLE_NAME', table.table_name)

        api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi", handler=handler)
