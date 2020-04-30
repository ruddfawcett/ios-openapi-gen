import Foundation
import Alamofire

final class Client: NSObject {
    private let session: Alamofire.Session
    public let baseURL: URL = URL(string: "")!
    private let queue: DispatchQueue = .main

    public var token: String?

    init(accessToken: String) {
        self.token = accessToken

        let headers = HTTPHeaders([
            HTTPHeader(name: "Authorization", value: "Bearer \(accessToken)"),
            HTTPHeader(name: "Accept", value: "application/json"),
            HTTPHeader(name: "Content-Type", value: "application/json"),
            HTTPHeader(name: "Access-Control-Allow-Origin", value: "*"),
            HTTPHeader(name: "User-Agent", value: "SATURN-CLIENT"),
            HTTPHeader(name: "Accept-Encoding", value: "gzip, deflate"),
            HTTPHeader(name: "Connection", value: "keep-alive"),
        ])

        let configuration = URLSessionConfiguration.default
        configuration.headers = headers
        configuration.timeoutIntervalForResource = 15
        configuration.httpMaximumConnectionsPerHost = 4

        let serverTrustManager = ServerTrustManager(evaluators: [self.baseURL.host!: DisabledEvaluator()])
        self.session = Alamofire.Session(configuration: configuration, serverTrustManager: serverTrustManager)
    }

    func request<Response>(_ endpoint: Endpoint<Response>, onSuccess: @escaping (Response) -> (), onFailure: @escaping(Error) -> ()) {
        let request = self.session.request(self.url(path: endpoint.path), method: endpoint.method, parameters: endpoint.parameters, encoding: JSONEncoding.default)
        request.validate().response(queue: self.queue) { response in
            if let error = response.error {
                onFailure(error)
            }

            guard let data = response.data else {
                return onFailure(response.error!)
            }

            do {
                let model = try endpoint.decode(data)
                return onSuccess(model)
            } catch let error {
                return onFailure(error)
            }
        }
    }

    private func url(path: SCPath) -> URL {
        return baseURL.appendingPathComponent(path)
    }
}
