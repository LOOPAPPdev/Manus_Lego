import { z } from 'zod';

/**
 * Contracts for the governance plane: quality gates (G0–G6), requirement
 * traceability and evidence records.
 *
 * NIST SP 800-218 (SSDF) practices are *mapped* to these artifacts. A passing
 * gate is evidence of an implemented control, never a claim of certification.
 */

export const SsdfPracticeSchema = z.enum(['PO', 'PS', 'PW', 'RV']);
export type SsdfPractice = z.infer<typeof SsdfPracticeSchema>;

export const GateIdSchema = z.enum(['G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6']);
export type GateId = z.infer<typeof GateIdSchema>;

export const GateStatusSchema = z.enum(['pass', 'fail', 'blocked', 'not_evaluated']);
export type GateStatus = z.infer<typeof GateStatusSchema>;

export const GateResultSchema = z.object({
  id: GateIdSchema,
  name: z.string(),
  status: GateStatusSchema,
  detail: z.string(),
  evidence: z.array(z.string()),
  requirement_ids: z.array(z.string()),
});
export type GateResult = z.infer<typeof GateResultSchema>;

export const GateReportSchema = z.object({
  schema_version: z.literal('1.0.0'),
  generated_at: z.string(),
  commit: z.string(),
  environment: z.string(),
  overall: GateStatusSchema,
  gates: z.array(GateResultSchema),
});
export type GateReport = z.infer<typeof GateReportSchema>;

export const RequirementStatusSchema = z.enum(['verified', 'partial', 'unverified', 'failing']);
export type RequirementStatus = z.infer<typeof RequirementStatusSchema>;

export const RequirementSchema = z.object({
  id: z.string().regex(/^REQ-(PO|PS|PW|RV)-\d{3}$/),
  practice: SsdfPracticeSchema,
  title: z.string(),
  statement: z.string(),
  acceptance: z.array(z.string()).min(1),
  implementation: z.array(z.string()),
  tests: z.array(z.string()),
  evidence: z.array(z.string()),
  manual_control: z.boolean().optional(),
});
export type Requirement = z.infer<typeof RequirementSchema>;

export const TraceabilityFileSchema = z.object({
  schema_version: z.string(),
  requirements: z.array(RequirementSchema),
});
export type TraceabilityFile = z.infer<typeof TraceabilityFileSchema>;

export const TestOutcomeSchema = z.object({
  nodeid: z.string(),
  name: z.string(),
  outcome: z.enum(['passed', 'failed', 'skipped', 'error']),
  duration: z.number().nonnegative(),
  requirement_ids: z.array(z.string()),
});

export const RequirementResultSchema = z.object({
  id: z.string(),
  practice: SsdfPracticeSchema,
  title: z.string(),
  status: RequirementStatusSchema,
  implementation_present: z.boolean(),
  missing_implementation: z.array(z.string()),
  tests: z.array(TestOutcomeSchema),
  evidence: z.array(z.string()),
  manual_control: z.boolean(),
  notes: z.array(z.string()),
});

export const TraceabilityReportSchema = z.object({
  schema_version: z.literal('1.0.0'),
  generated_at: z.string(),
  commit: z.string(),
  requirements: z.array(RequirementResultSchema),
  summary: z.object({
    total: z.number().int(),
    verified: z.number().int(),
    partial: z.number().int(),
    unverified: z.number().int(),
    failing: z.number().int(),
    by_practice: z.record(z.string(), z.number().int()),
  }),
});
export type TraceabilityReport = z.infer<typeof TraceabilityReportSchema>;

export const EvidenceRecordSchema = z.object({
  id: z.string(),
  kind: z.enum(['gate_report', 'traceability', 'test_run', 'security_scan', 'catalog_snapshot', 'decision']),
  created_at: z.string(),
  commit: z.string(),
  producer: z.string(),
  subject: z.array(z.string()),
  sha256: z.string().regex(/^[a-f0-9]{64}$/),
  path: z.string(),
});
export type EvidenceRecord = z.infer<typeof EvidenceRecordSchema>;
