# Reference investigation with REA

The user requested [morluto/rea](https://github.com/morluto/rea). REA **6.7.0 was downloaded and executed**, not merely listed as a suggested tool. It inspected the public [AI Engineering from Scratch homepage](https://aiengineeringfromscratch.com/) in an isolated Chromium profile.

## Retained evidence

- File: [rea-reference-page.json](rea-reference-page.json)
- Evidence ID: `ev_80ad372b01e7bb6fd86149b2a03dc108db4788399a78dc29398a31c8c3e5c52b`
- SHA-256 of the saved file: `b4ba31113183a011be2d3ecaebe654b2bbc240c6a89d5e5a472f6046e45972e0`
- Provider: `rea-cdp-browser`
- Browser: `Chrome/152.0.7977.82`
- DOM nodes reported: 1853
- Accessibility nodes reported: 1011
- Script records reported: 14
- Capture status: `policy_filtered`

The capture includes accessible labels and structure. It requests storage **key names**, never storage values. The fresh profile contained a star-nudge key and a repository-star cache key; this does **not** establish the reference site's learner-progress implementation.

## Reproduction

Launch a disposable Chromium profile with a loopback debugging port, then discover the current target ID:

```bash
chromium --remote-debugging-address=127.0.0.1 --remote-debugging-port=9231 --user-data-dir=/tmp/ece-rea-browser https://aiengineeringfromscratch.com/
npx --yes rea-agents@6.7.0 list-browser-targets http://127.0.0.1:9231 --json
```

Use the ID returned by discovery, not an ID from another browser session:

```text
npx --yes rea-agents@6.7.0 inspect-web-page http://127.0.0.1:9231 TARGET_ID --include-accessibility-text --include-storage-keys --json
```

The actual capture selected target `9B8BE2BBC8EC0D33BAFDC61A93D14AF9`. Its result is saved above. REA was run using a temporary npm cache; global agent configuration and MCP registrations were not changed.

## What informed this implementation

The observed homepage exposes a clear course entry point, focused learning paths, expandable phase navigation, and a terminal-tutoring route. Those observations informed four independent choices here: a visible start/resume link, prerequisite-aware ECE tracks, expandable modules, and a local tutor skill. The ECE site adds its own numerical workbench and learner-owned notes; those are original implementations, not claims recovered from upstream source.

## Limits

REA attached after page load, so earlier network and console activity was not observed. Script sources were not requested. Cross-origin resources were filtered. The capture reports no truncated or unavailable sections, but its policy and attachment limits remain. This is not a source-code audit, full interaction trace, visual clone, or proof of the reference site's internal architecture.

The raw observation is retained for traceability and contains third-party public-page labels. Those labels remain attributable to the reference project. They were not used as ECE lesson prose. See the [upstream repository](https://github.com/rohitg00/ai-engineering-from-scratch) for its licensing and authorship.
