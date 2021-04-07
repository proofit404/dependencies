export default async (): undefined => {
  if (danger.github.pr.commits > 3) {
    fail("PR has too much commits");
    return;
  }

  if (danger.github.pr.labels.length > 0) {
    fail("PR is not allowed to have labels");
    return;
  }

  if (danger.github.pr.milestone) {
    fail("PR is not allowed to have milestone");
    return;
  }

  if (danger.github.pr.assignee?.id !== danger.github.pr.user.id) {
    fail("Only PR author could be assigned to PR");
    return;
  }

  const commitTest = danger.git.commits.map((commit) =>
    commit.message.match(/^(\w+):/)
  );

  if (!commitTest.every((match) => match)) {
    fail("Unable to analyze commit types");
    return;
  }

  const commitTypes = new Set(commitTest.map((commitMatch) => commitMatch[1])),
    hasFeatureCommit = commitTypes.has("feat"),
    hasFixCommit = commitTypes.has("fix"),
    hasDocsCommit = commitTypes.has("docs"),
    hasTestCommit = commitTypes.has("test");

  const hasBreakingCommit = danger.git.commits
    .map((commit) => commit.message.match(/\sBREAKING CHANGE:\s/g))
    .some((match) => match);

  if (commitTest.length !== commitTypes.size) {
    fail("PR can not contain commits with the same type");
    return;
  }

  const commitFiles = danger.git.created_files
      .concat(danger.git.modified_files)
      .concat(danger.git.deleted_files),
    hasDocsChanges = commitFiles.some(
      (fileName) => fileName.startsWith("docs/") || fileName === "mkdocs.yml"
    ),
    hasTestChanges = commitFiles.some(
      (fileName) => fileName.startsWith("tests/") || fileName === "pytest.ini"
    ),
    hasSourceChanges = commitFiles.some(
      (fileName) => fileName.startsWith("src/") || fileName === "pyproject.toml"
    );

  if (hasDocsCommit & !hasDocsChanges) {
    fail("Commit with the 'docs' type should change documentation files");
    return;
  }

  if (hasTestCommit & !hasTestChanges) {
    fail("Commit with the 'test' type should change test files");
    return;
  }

  if (hasFixCommit & !hasSourceChanges) {
    fail("Commit with the 'fix' type should change source files");
    return;
  }

  if (hasFeatureCommit & !hasSourceChanges) {
    fail("Commit with the 'feat' type should change source files");
    return;
  }

  const branchTest = danger.github.pr.head.ref.match(/^issue-(\d+)$/);

  if (!branchTest) {
    fail("Branch name should be 'issue-N' where N is the issue number");
    return;
  }

  const issueNumber = branchTest[1];

  for (const commit of danger.git.commits) {
    if (!commit.message.split(/\r?\n/)[0].endsWith(` #${issueNumber}`)) {
      fail("The first line of each commit should ends with the issue number");
      return;
    }
  }

  if (danger.github.pr.body) {
    fail("PR body should be empty");
    return;
  }

  const issueJSON = await danger.github.api.issues.get({
    owner: danger.github.thisPR.owner,
    repo: danger.github.thisPR.repo,
    issue_number: parseInt(issueNumber),
  });

  if (issueJSON.status !== 200) {
    fail(`Unable to check issue #${issueNumber}`);
    return;
  }

  if (issueJSON.data.closed_at) {
    fail("Closed issue can't be implemented");
    return;
  }

  if (issueJSON.data.milestone) {
    if (issueJSON.data.milestone.closed_at) {
      fail("Issues of closed milestone can't be implemented");
      return;
    }
  }

  if (issueJSON.data.assignee) {
    fail("Issue can't have an assignee");
    return;
  }

  const issueLabels = new Set(issueJSON.data.labels.map((label) => label.name)),
    hasIncompatibleLabel = issueLabels.has("backward incompatible"),
    hasFeatureLabel = issueLabels.has("feature"),
    hasBugLabel = issueLabels.has("bug"),
    hasDocumentationLabel = issueLabels.has("documentation");

  if (hasFeatureLabel & hasBugLabel) {
    fail("An issue can't be a bug and a feature simultaneously");
    return;
  }

  if (hasIncompatibleLabel ^ hasBreakingCommit) {
    fail(
      "Only issue marked as backward incompatible is allowed to have breaking changes"
    );
    return;
  }

  if (hasFeatureLabel ^ hasFeatureCommit) {
    fail("Only issue marked as feature is allowed to have feat commit");
    return;
  }

  if (hasBugLabel ^ hasFixCommit) {
    fail("Only issue marked as bug is allowed to have fix commit");
    return;
  }

  if (hasDocumentationLabel & !hasDocsCommit) {
    fail("Issue marked as documentation should have docs commit");
    return;
  }

  if (hasFeatureLabel & !hasDocsCommit) {
    fail("Issue marked as feature should have docs commit");
    return;
  }

  for (const label of [
    "blocked",
    "invalid",
    "needs investigation",
    "question",
    "wontfix",
  ]) {
    if (issueLabels.has(label)) {
      fail(`Issues marked as ${label} can not be implemented`);
      return;
    }
  }

  const issueText = issueJSON.data.body,
    issueLines = issueText.split(/\r?\n/).map((line) => line.trim());

  for (const line of issueLines) {
    if (line.match(/^[*+-] \[[xX]\] /)) {
      fail("Create a milestone instead of the issue with the task list");
      return;
    }
  }

  const labelsJSON = await danger.github.api.issues.listLabelsForRepo({
    owner: danger.github.thisPR.owner,
    repo: danger.github.thisPR.repo,
  });

  if (labelsJSON.status !== 200) {
    fail("Unable to check repository labels");
    return;
  }

  const allowedLabels = new Set([
    "backward incompatible",
    "blocked",
    "bug",
    "documentation",
    "feature",
    "invalid",
    "needs investigation",
    "question",
    "released",
    "wontfix",
  ]);

  for (const repoLabel of labelsJSON.data) {
    if (repoLabel.color !== "ededed") {
      fail(`The color of the ${repoLabel.name} should be 'ededed'`);
      return;
    } else if (repoLabel.description !== "") {
      fail(`The description of the ${repoLabel.name} should be empty`);
      return;
    } else if (!allowedLabels.has(repoLabel.name)) {
      fail(`Unknown label ${repoLabel.name}`);
      return;
    }
  }

  const milestonesJSON = await danger.github.api.issues.listMilestonesForRepo({
    owner: danger.github.thisPR.owner,
    repo: danger.github.thisPR.repo,
  });

  if (milestonesJSON.status !== 200) {
    fail("Unable to check repository milestones");
    return;
  }

  for (const milestone of milestonesJSON.data) {
    if (milestone.description !== "") {
      fail(`The description of the ${milestone.title} should be empty`);
      return;
    } else if (milestone.due_on) {
      fail(`The due date of the ${milestone.title} should not be set`);
      return;
    }
  }
};
