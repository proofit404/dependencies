export default async () => {
  if (danger.github.pr.commits > 3) {
    fail("PR has too much commits");
    return;
  }

  if (danger.github.pr.labels.length > 0) {
    fail("PR is not allowed to have labels");
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
    hasDocsCommit = commitTypes.has("docs");

  if (commitTest.length !== commitTypes.size) {
    fail("PR can not contain commits with the same type");
    return;
  }

  const branchTest = danger.github.pr.head.ref.match(/^issue-(\d+)$/);

  if (!branchTest) {
    fail("Branch name should be 'issue-N' where N is the issue number");
    return;
  }

  const issueNumber = branchTest[1];

  if (`Fix #${issueNumber}` !== danger.github.pr.body.trim()) {
    fail("PR body should be 'Fix #N' where N is the issue number");
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

  if (issueJSON.data.assignee) {
    fail("Issue can't have an assignee");
    return;
  }

  const issueLabels = new Set(issueJSON.data.labels.map((label) => label.name)),
    hasFeatureLabel = issueLabels.has("feature"),
    hasBugLabel = issueLabels.has("bug"),
    hasDocumentationLabel = issueLabels.has("documentation");

  if (hasFeatureLabel & hasBugLabel) {
    fail("An issue can't be a bug and a feature simultaneously");
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

  for (let label of [
    "blocked",
    "invalid",
    "needs-investigation",
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

  for (let line of issueLines) {
    if (line.match(/^[-\+\*] \[[xX]\] /)) {
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

  for (let repoLabel of labelsJSON.data) {
    if (repoLabel.color !== "ededed") {
      fail(`The color of the ${repoLabel.name} should be 'ededed'`);
      return;
    } else if (repoLabel.description !== "") {
      fail(`The description of the ${repoLabel.name} should be empty`);
      return;
    }
  }
};
