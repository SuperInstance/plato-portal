/**
 * SuperInstance Fleet Schema Registry
 * Re-exports all schema types for the fleet
 */

export const SCHEMA_VERSION = '1.0.0';

// Fleet Health
export { type ServiceStatus, type AgentStatus, type HealthReport } from './fleet-health';

// Constraint Model
export { type Constraint, type MutableConstraintModel, type OverridePattern, type OverrideEvent, type DecisionDelta, type ConstraintOperator } from './constraint-model';

// Productive Lane
export { type IntentGoal, type IntentSignal, type NavigationPattern, type NavigationStep, type RetryPolicy, type ProductiveLane } from './productive-lane';

// Quality Score
export { type TileQualityLabel, type QualityScore } from './quality-score';

// Trust Vector
export { type TrustVector, type TrustHistoryEntry, type VesselIdentity, type FleetGraph, type FleetNode, type FleetEdge } from './trust-vector';

// Turbo Shell
export { ShellType, Capability, type TurboManifest } from './turbo-shell';

// PLATO Tile
export { type RoomMetadata, type PlatoTile, type SubmitResponse, type ErrorResponse, type SubmitResult } from './plato-tile';
