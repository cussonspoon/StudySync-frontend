from PySide6.QtCore import QObject, Signal, QEventLoop, QUrl, QByteArray, QUrlQuery, QJsonDocument
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QSslConfiguration, QSsl
from types import FunctionType


class BaseController(QObject):
    api_response_received = Signal(str)  # Signal to notify when data is received
    api_error_occurred = Signal(str)    # Signal for error handling
    SERVER_URL = "http://localhost:8000"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager()
        self.ssl_config = QSslConfiguration()
        self.ssl_config.setProtocol(QSsl.TlsV1_2OrLater)

    def check_reply_error(self, reply: QNetworkReply):
        """Check if the network reply contains an error and emit a signal if it does."""
        if reply.error() != QNetworkReply.NoError:
            error_message = reply.errorString()
            self.api_error_occurred.emit(error_message)
            print(f"Network error: {error_message}")
            raise Exception(f"Network error: {reply.error()} - {error_message}")

    def perform_get_request_sync(self, url: str, data: dict = None, headers: dict = None) -> QNetworkReply:
        """Perform a synchronous GET request."""
        request_url = QUrl(url)

        if data:
            query_params = QUrlQuery()
            for key, value in data.items():
                query_params.addQueryItem(str(key), str(value))
            request_url.setQuery(query_params)

        request = QNetworkRequest(request_url)
        request.setSslConfiguration(self.ssl_config)

        if headers:
            for key, value in headers.items():
                request.setRawHeader(QByteArray(key.encode()), QByteArray(str(value).encode()))

        reply = self.network_manager.get(request)

        # Wait for the reply to finish
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()

        self.check_reply_error(reply)
        return reply

    def perform_get_request_async(self, url: str, data: dict = None, callback: FunctionType = None, headers: dict = None):
        """Perform an asynchronous GET request."""
        request_url = QUrl(url)

        if data:
            query_params = QUrlQuery()
            for key, value in data.items():
                query_params.addQueryItem(str(key), str(value))
            request_url.setQuery(query_params)

        request = QNetworkRequest(request_url)
        request.setSslConfiguration(self.ssl_config)

        if headers:
            for key, value in headers.items():
                request.setRawHeader(QByteArray(key.encode()), QByteArray(str(value).encode()))

        # Connect the finished signal to the handler
        if callback:
            self.network_manager.finished.connect(lambda reply: self.handle_response(reply, callback))

        reply = self.network_manager.get(request)
        return reply

    def perform_post_request_async(self, url: str, data: dict = None, callback: FunctionType = None, headers: dict = None):
        """Perform an asynchronous POST request."""
        request_url = QUrl(url)
        request = QNetworkRequest(request_url)
        request.setSslConfiguration(self.ssl_config)

        if headers:
            for key, value in headers.items():
                request.setRawHeader(QByteArray(key.encode()), QByteArray(str(value).encode()))

        if data is None:
            data = {}

        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        request_body = QJsonDocument.fromVariant(data).toJson()

        # Connect the finished signal to the handler
        if callback:
            self.network_manager.finished.connect(lambda reply: self.handle_response(reply, callback))

        reply = self.network_manager.post(request, request_body)
        return reply

    def perform_post_request_sync(self, url: str, data: dict = None, headers: dict = None, is_json: bool = True) -> QNetworkReply:
        """Perform a synchronous POST request."""
        request_url = QUrl(url)
        request = QNetworkRequest(request_url)
        request.setSslConfiguration(self.ssl_config)

        if headers:
            for key, value in headers.items():
                request.setRawHeader(QByteArray(key.encode()), QByteArray(str(value).encode()))

        if data is None:
            data = {}

        if is_json:
            request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
            request_body = QJsonDocument.fromVariant(data).toJson()
        else:
            request_body = QByteArray(data.encode() if isinstance(data, str) else str(data).encode())

        reply = self.network_manager.post(request, request_body)

        # Wait for the reply to finish
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()

        self.check_reply_error(reply)
        return reply

    def handle_response(self, reply: QNetworkReply, callback: FunctionType):
        """Handle the response from an asynchronous request."""
        self.check_reply_error(reply)
        if callback:
            callback(reply)
        reply.deleteLater()
        # Disconnect the signal to avoid multiple triggers
        try:
            self.network_manager.finished.disconnect()
        except TypeError:
            pass  # Signal was already disconnected