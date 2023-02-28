import XCTest
@testable import AnyTest

public final class AnyTestPublicFinalTests: XCTestCase {
  func testExample() {
    XCTAssertEqual(AnyTest().text, "Hello, World!")
  }

  static var allTests = [
    ("testExample", testExample),
  ]
}
