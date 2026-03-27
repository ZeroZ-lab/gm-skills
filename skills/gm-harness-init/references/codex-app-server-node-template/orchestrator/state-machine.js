const ALLOWED_TRANSITIONS = {
  idle: ["generating", "failed"],
  generating: ["evaluating", "failed"],
  evaluating: ["done", "generating", "failed"],
  failed: ["generating"],
  done: ["generating"]
};

function assertTransition(fromPhase, toPhase) {
  const allowed = ALLOWED_TRANSITIONS[fromPhase] || [];

  if (!allowed.includes(toPhase)) {
    throw new Error(`invalid state transition: ${fromPhase} -> ${toPhase}`);
  }
}

module.exports = {
  ALLOWED_TRANSITIONS,
  assertTransition
};
