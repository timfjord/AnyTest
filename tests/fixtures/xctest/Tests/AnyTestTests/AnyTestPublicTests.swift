import XCTest
@testable import AnyTest

public class AnyTestPublicTests: XCTestCase {
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
