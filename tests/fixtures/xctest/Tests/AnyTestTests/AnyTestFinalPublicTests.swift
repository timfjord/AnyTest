import XCTest
@testable import AnyTest

final public class AnyTestFinalPublicTests: XCTestCase {
  func testExample() {
    XCTAssertEqual(AnyTest().text, "Hello, World!")
  }

  static var allTests = [
    ("testExample", testExample),
  ]
}
