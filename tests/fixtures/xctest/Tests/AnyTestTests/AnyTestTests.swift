import XCTest
@testable import AnyTest

class AnyTestTests: XCTestCase {
  func testExample() {
    XCTAssertEqual(AnyTest().text, "Hello, World!")
  }

  func testOther() {
    XCTAssertEqual(true, true)
  }

  static var allTests = [
    ("testExample", testExample),
    ("testOther", testOther)
  ]
}
