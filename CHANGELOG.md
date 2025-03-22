# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-03-22

### Fixed

- Fixed edge case where spaces were missing between adjacent text nodes.

### Add

- Added Python compatibility

## [0.2.0] - 2024-07-16

### Added

- New methods `edit_page_md_append_to_front` and `edit_page_md_append_to_back` for appending content to existing pages
- Retry mechanism in `get_page` method with customizable max retries and delay
- Custom error content generation for failed page retrievals
- More comprehensive docstrings following Google style guide

### Changed

- `edit_page` and `edit_page_md` methods now accept an optional `title` parameter
- Improved error handling in various methods
- Refactored code for better reusability and maintainability

### Fixed

- Issue with title retrieval in `edit_page` when no new title is provided

## [0.1.0] - 2024-07-14

### Added

- Initial release of YTelegraph
- Basic functionality for interacting with the Telegraph API
- Support for creating and editing Telegraph pages
- Markdown to Telegraph DOM conversion
- Simple account management features
- Token handling and storage

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A