module.exports = {
  repositoryUrl: "https://github.com/proofit404/dependencies",
  branches: ["release", { name: "develop", prerelease: "rc" }],
  tagFormat: "${version}",
  plugins: [
    "@semantic-release/commit-analyzer",
    [
      "@semantic-release/release-notes-generator",
      {
        linkCompare: false,
        linkReferences: false,
      },
    ],
    [
      "@semantic-release/changelog",
      {
        changelogFile: "docs/changelog.md",
      },
    ],
    [
      "@semantic-release/exec",
      {
        prepareCmd:
          "./scripts/lint && poetry version ${nextRelease.version} && npm version ${nextRelease.version} && poetry build",
        publishCmd: "poetry publish",
      },
    ],
    [
      "@semantic-release/git",
      {
        assets: ["docs/changelog.md", "pyproject.toml"],
      },
    ],
    [
      "@semantic-release/github",
      {
        assets: [{ path: "dist/*.whl" }, { path: "dist/*.tar.gz" }],
      },
    ],
  ],
};
