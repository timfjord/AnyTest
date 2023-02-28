import XCTest
@testable import AnyTest

final class AnyTestFinalTests: XCTestCase {
  func testExample() {
    XCTAssertEqual(AnyTest().text, "Hello, World!")
  }

  static var allTests = [
    ("testExample", testExample),
  ]
}
