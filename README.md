# ios-openapi-gen
🎁 Wrap Swagger OpenAPIs with an API pattern developed by [@kean](https://kean.github.io/post/api-client). Right now the project will do everything but function names, but will tackle that soon.

## Usage
- 🧑‍💻 grab latest `openapi.json`
- 📝 edit settings in `settings.yml`
- 🛠 run `python gen.py`
- 🔎 go to `output/*`
- 😎 use generated Swift API layer

## Example Output

```swift
extension API {
    enum Store {}
}

extension API.Store {

    /// Returns pet inventories by status
    static func <# Readable Name #>() -> Endpoint<<# Model Type/Void #>> {
        return Endpoint(method: .get, path: "/store/inventory")
    }

    /// Place an order for a pet
    static func <# Readable Name #>() -> Endpoint<<# Model Type/Void #>> {
        return Endpoint(method: .post, path: "/store/order")
    }

    /// Find purchase order by id
    static func <# Readable Name #>(orderId: Int) -> Endpoint<<# Model Type/Void #>> {
        return Endpoint(method: .get, path: "/store/order/\(orderId)")
    }

    /// Delete purchase order by id
    static func <# Readable Name #>(orderId: Int) -> Endpoint<<# Model Type/Void #>> {
        return Endpoint(method: .delete, path: "/store/order/\(orderId)")
    }

}
```

## Future Plans
- 🤡 parse full documentation for paths
- 📖 generate semi-readable API function names
- 🤗 handle body parameters
- 🖼 support framework/patterns beyond Alamofire

## Colophon
- [@ruddfawcett](https://github.com/ruddfawcett): Python parser and converter for OpenAPIs.
- [@kean](https://kean.github.io/post/api-client): API layer concept, originally written with Alamofire and RxSwift.
