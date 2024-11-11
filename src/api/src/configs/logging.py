import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from datetime import datetime, timezone

from .settings import settings

# Credenciais AWS da configuração
ACCESS_KEY_AWS = settings.ACCESS_KEY_AWS
SECRET_KEY_AWS = settings.SECRET_KEY_AWS
SESSION_TOKEN_AWS = settings.SESSION_TOKEN_AWS


class CloudWatchLoggerHandler(logging.Handler):
    def __init__(self, log_group: str, log_stream: str, aws_region: str = 'us-east-1'):
        super().__init__()
        self.log_group = log_group
        self.log_stream = log_stream
        self.aws_region = aws_region

        self.sequence_token = None

        try:
            # Tenta criar o cliente do CloudWatch Logs com boto3
            self.client = boto3.client(
                'logs',
                region_name=self.aws_region,
                aws_access_key_id=ACCESS_KEY_AWS,
                aws_secret_access_key=SECRET_KEY_AWS,
                aws_session_token=SESSION_TOKEN_AWS
            )
            self._create_log_group()
            self._create_log_stream()
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Erro de credenciais da AWS: {e}")
            self.client = None  # Define o cliente como None para evitar outros erros
        except ClientError as e:
            print(f"Erro ao criar cliente CloudWatch: {e}")
            self.client = None
        pass

    def _create_log_group(self):
        if self.client:
            # Tenta criar o Log Group se ele não existir
            try:
                self.client.create_log_group(logGroupName=self.log_group)
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    print(f"Erro ao criar log group: {e}")
        pass

    def _create_log_stream(self):
        if self.client:
            # Tenta criar o Log Stream se ele não existir
            try:
                self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    print(f"Erro ao criar log stream: {e}")
        pass

    def emit(self, record):
        if not self.client:
            print("Cliente do CloudWatch Logs não disponível. Log não enviado.")
            return

        # Envia o log formatado para o CloudWatch
        utc_now = datetime.now(timezone.utc)
        formatted_message = self.format(record)

        log_event = {
            'logGroupName': self.log_group,
            'logStreamName': self.log_stream,
            'logEvents': [{
                'timestamp': int(utc_now.timestamp() * 1000),  # Converte para milissegundos
                'message': formatted_message
            }]
        }

        if self.sequence_token:
            log_event['sequenceToken'] = self.sequence_token

        try:
            response = self.client.put_log_events(**log_event)
            # Atualiza o sequence token
            self.sequence_token = response.get('nextSequenceToken')
        except ClientError as e:
            print(f"Erro ao enviar log para o CloudWatch: {e}")
        pass


class Logger:
    def __init__(self, log_group: str, log_stream: str, level=logging.DEBUG):
        # Cada log stream terá seu próprio logger
        # Logger separado para cada log stream
        self.logger = logging.getLogger(f"{log_group}_{log_stream}")
        # Certifique-se de que o nível do logger seja DEBUG
        self.logger.setLevel(level)

        aws_region = 'us-east-1'

        # Configura o handler para enviar logs para o CloudWatch
        cloudwatch_handler = CloudWatchLoggerHandler(
            log_group=log_group,
            log_stream=log_stream,
            aws_region=aws_region
        )

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        cloudwatch_handler.setFormatter(formatter)
        # Certifique-se de que o nível do handler seja DEBUG
        cloudwatch_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(cloudwatch_handler)

        # Adicionando o nível de log personalizado 'SUCCESS' se ainda não estiver registrado
        if not hasattr(logging, 'SUCCESS'):
            # Define um novo nível de log entre INFO (20) e WARNING (30)
            logging.SUCCESS = 25
            logging.addLevelName(logging.SUCCESS, 'SUCCESS')

            def success(self, message, *args, **kwargs):
                if self.isEnabledFor(logging.SUCCESS):
                    self._log(logging.SUCCESS, message, args, **kwargs)

            logging.Logger.success = success
        pass

    def log(self, level: str, msg: str):
        if level == "debug":
            self.logger.debug(msg)
        elif level == "info":
            self.logger.info(msg)
        elif level == "warning":
            self.logger.warning(msg)
        elif level == "error":
            self.logger.error(msg)
        elif level == "critical":
            self.logger.critical(msg)
        pass
