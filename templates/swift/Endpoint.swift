import Foundation
import Alamofire

typealias Parameters = [String: Any]
typealias Path = String

final class Endpoint<Response> {
    let method: HTTPMethod
    let path: Path
    let parameters: Parameters?
    let decode: (Data) throws -> Response

    init(method: HTTPMethod = .get, path: SCPath, parameters: SCParameters? = nil, decode: @escaping (Data) throws -> Response) {
        self.method = method
        self.path = path
        self.parameters = parameters
        self.decode = decode
    }
}

extension Endpoint where Response: Codable {
    convenience init(method: HTTPMethod = .get, path: SCPath, parameters: SCParameters? = nil) {
        self.init(method: method, path: path, parameters: parameters) {
            let decoder = JSONDecoder()
            return try decoder.decode(Response.self, from: $0)
        }
    }
}

extension Endpoint where Response == Void {
    convenience init(method: HTTPMethod = .get, path: SCPath, parameters: SCParameters? = nil) {
        self.init(method: method, path: path, parameters: parameters, decode: { _ in () } )
    }
}
