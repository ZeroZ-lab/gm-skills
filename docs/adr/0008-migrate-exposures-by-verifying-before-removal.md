# Migrate Exposures by verifying before removal

When a Runtime-native Plugin format becomes available for a Capability currently exposed through `npx skills`, the Manager reports the migration opportunity but does not apply it automatically. After Operator confirmation, it installs the native Plugin Exposure, completes Registry Verification, Discovery Verification, and Invocation Verification, and only then removes the old `npx skills` Exposure for that Runtime. Failure at any step preserves the existing working Exposure, and other Runtime Installations remain untouched.
