// Baobab Audit Trail and Approval Workflow
// Implements §48-49 of the Canonical Mapping Model: four-eyes approval and immutable audit logging.

import { v4 as uuidv4 } from 'uuid';

/**
 * Audit event type enumeration
 */
export type AuditEventType =
  | 'mapping.created'
  | 'mapping.updated'
  | 'mapping.validated'
  | 'mapping.activated'
  | 'mapping.suspended'
  | 'mapping.retired'
  | 'market.created'
  | 'market.updated'
  | 'market.activated'
  | 'tenant.created'
  | 'tenant.provisioned'
  | 'tenant.suspended'
  | 'approval.requested'
  | 'approval.granted'
  | 'approval.denied';

/**
 * Audit log entry (§49)
 *
 * Every mutation MUST record:
 * - who (actor_id)
 * - what (resource_type, resource_id, changes)
 * - when (action_timestamp)
 * - tenant (tenant_id)
 * - previous value (previous_state)
 * - new value (new_state)
 * - reason (reason)
 * - request ID (request_id)
 * - correlation ID (correlation_id)
 */
export interface AuditLogEntry {
  audit_id: string;
  event_type: AuditEventType;
  tenant_id: string;
  legal_entity_id?: string;
  resource_type: 'mapping' | 'market' | 'tenant' | 'estate' | 'context' | 'approval';
  resource_id: string;
  actor_id: string;
  actor_type: 'user' | 'service_account' | 'system';
  action_timestamp: Date;
  request_id: string;
  correlation_id: string;
  causation_id?: string;
  previous_state?: any;
  new_state?: any;
  changes?: Record<string, { from: any; to: any }>;
  reason?: string;
  approval_id?: string;
  origin?: string;
  http_method?: string;
  http_path?: string;
  http_status?: number;
  success: boolean;
  error_code?: string;
  error_message?: string;
  metadata?: Record<string, any>;
}

/**
 * Approval decision (§48)
 */
export interface ApprovalDecision {
  approver_id: string;
  decision: 'approved' | 'denied';
  approved_at: Date;
  comment?: string;
}

/**
 * Approval workflow (§48: four-eyes approval for critical mappings)
 *
 * Critical mappings that should require four-eyes approval:
 * - Accounting mappings
 * - Tax mappings
 * - Payment mappings
 * - Cross-tenant mappings
 * - ERP organisation mappings
 * - Data-residency bindings
 */
export interface ApprovalRequest {
  approval_id: string;
  approval_type: 'four_eyes' | 'legal_review' | 'security_review' | 'policy_review';
  resource_type: 'mapping' | 'market' | 'tenant';
  resource_id: string;
  tenant_id: string;
  requester_id: string;
  description: string;
  rationale?: string;
  required_approvers: number;
  status: 'pending' | 'in_progress' | 'approved' | 'denied' | 'cancelled';
  approvals: ApprovalDecision[];
  denied_reason?: string;
  expires_at: Date;
  created_at: Date;
  updated_at: Date;
  completed_at?: Date;
}

/**
 * Audit trail context (passed through request)
 */
export interface AuditContext {
  tenant_id: string;
  actor_id: string;
  actor_type?: 'user' | 'service_account' | 'system';
  request_id: string;
  correlation_id: string;
  causation_id?: string;
  origin?: string;
  http_method?: string;
  http_path?: string;
}

/**
 * Baobab Audit Trail Manager
 *
 * Manages immutable audit logs and approval workflows
 */
export class AuditTrailManager {
  private auditLog: Map<string, AuditLogEntry> = new Map();
  private approvalWorkflows: Map<string, ApprovalRequest> = new Map();

  /**
   * Record an audit event (§49)
   *
   * All mutations must go through this path.
   */
  recordAuditEvent(params: {
    event_type: AuditEventType;
    context: AuditContext;
    resource_type: string;
    resource_id: string;
    previous_state?: any;
    new_state?: any;
    reason?: string;
    approval_id?: string;
    http_status?: number;
    success: boolean;
    error?: { code: string; message: string };
  }): AuditLogEntry {
    const entry: AuditLogEntry = {
      audit_id: `audit_${this.generateId()}`,
      event_type: params.event_type,
      tenant_id: params.context.tenant_id,
      resource_type: params.resource_type as any,
      resource_id: params.resource_id,
      actor_id: params.context.actor_id,
      actor_type: params.context.actor_type || 'user',
      action_timestamp: new Date(),
      request_id: params.context.request_id,
      correlation_id: params.context.correlation_id,
      causation_id: params.context.causation_id,
      previous_state: params.previous_state,
      new_state: params.new_state,
      changes: this.computeChanges(params.previous_state, params.new_state),
      reason: params.reason,
      approval_id: params.approval_id,
      origin: params.context.origin,
      http_method: params.context.http_method,
      http_path: params.context.http_path,
      http_status: params.http_status,
      success: params.success,
      error_code: params.error?.code,
      error_message: params.error?.message,
    };

    // Store immutably (append-only from application perspective)
    this.auditLog.set(entry.audit_id, entry);

    return entry;
  }

  /**
   * Retrieve audit log entries with optional filtering
   */
  queryAuditLog(filters: {
    tenant_id?: string;
    resource_type?: string;
    resource_id?: string;
    actor_id?: string;
    event_type?: AuditEventType;
    from_timestamp?: Date;
    to_timestamp?: Date;
    success_only?: boolean;
    limit?: number;
  }): AuditLogEntry[] {
    const limit = filters.limit || 100;
    let results: AuditLogEntry[] = Array.from(this.auditLog.values());

    // Apply filters
    if (filters.tenant_id) {
      results = results.filter((e) => e.tenant_id === filters.tenant_id);
    }
    if (filters.resource_type) {
      results = results.filter((e) => e.resource_type === filters.resource_type);
    }
    if (filters.resource_id) {
      results = results.filter((e) => e.resource_id === filters.resource_id);
    }
    if (filters.actor_id) {
      results = results.filter((e) => e.actor_id === filters.actor_id);
    }
    if (filters.event_type) {
      results = results.filter((e) => e.event_type === filters.event_type);
    }
    if (filters.from_timestamp) {
      results = results.filter((e) => e.action_timestamp >= filters.from_timestamp!);
    }
    if (filters.to_timestamp) {
      results = results.filter((e) => e.action_timestamp <= filters.to_timestamp!);
    }
    if (filters.success_only) {
      results = results.filter((e) => e.success);
    }

    // Sort by timestamp descending and limit
    return results.sort((a, b) => b.action_timestamp.getTime() - a.action_timestamp.getTime()).slice(0, limit);
  }

  /**
   * Create an approval request for critical mappings (§48)
   *
   * Critical mappings that require four-eyes approval:
   * - Accounting
   * - Tax
   * - Payment
   * - Cross-tenant
   * - ERP organisation
   * - Data-residency
   */
  createApprovalRequest(params: {
    approval_type: 'four_eyes' | 'legal_review' | 'security_review' | 'policy_review';
    resource_type: 'mapping' | 'market' | 'tenant';
    resource_id: string;
    tenant_id: string;
    requester_id: string;
    description: string;
    rationale?: string;
    required_approvers?: number;
    ttl_minutes?: number;
  }): ApprovalRequest {
    const approval: ApprovalRequest = {
      approval_id: `appr_${this.generateId()}`,
      approval_type: params.approval_type,
      resource_type: params.resource_type,
      resource_id: params.resource_id,
      tenant_id: params.tenant_id,
      requester_id: params.requester_id,
      description: params.description,
      rationale: params.rationale,
      required_approvers: params.required_approvers || 2,
      status: 'pending',
      approvals: [],
      expires_at: new Date(Date.now() + (params.ttl_minutes || 24 * 60) * 60 * 1000),
      created_at: new Date(),
      updated_at: new Date(),
    };

    this.approvalWorkflows.set(approval.approval_id, approval);
    return approval;
  }

  /**
   * Submit an approval decision
   */
  submitApprovalDecision(params: {
    approval_id: string;
    approver_id: string;
    decision: 'approved' | 'denied';
    comment?: string;
  }): ApprovalRequest {
    const approval = this.approvalWorkflows.get(params.approval_id);
    if (!approval) {
      throw new Error(`Approval ${params.approval_id} not found`);
    }

    if (approval.status !== 'pending' && approval.status !== 'in_progress') {
      throw new Error(`Approval ${params.approval_id} is in ${approval.status} state and cannot be modified`);
    }

    // Check for duplicate approvals from same approver
    if (approval.approvals.some((a) => a.approver_id === params.approver_id)) {
      throw new Error(`Approver ${params.approver_id} has already submitted a decision`);
    }

    const decision: ApprovalDecision = {
      approver_id: params.approver_id,
      decision: params.decision,
      approved_at: new Date(),
      comment: params.comment,
    };

    approval.approvals.push(decision);
    approval.status = 'in_progress';
    approval.updated_at = new Date();

    // Check completion conditions
    if (params.decision === 'denied') {
      approval.status = 'denied';
      approval.denied_reason = params.comment;
      approval.completed_at = new Date();
    } else if (approval.approvals.length >= approval.required_approvers) {
      const approvedCount = approval.approvals.filter((a) => a.decision === 'approved').length;
      if (approvedCount >= approval.required_approvers) {
        approval.status = 'approved';
        approval.completed_at = new Date();
      }
    }

    this.approvalWorkflows.set(approval.approval_id, approval);
    return approval;
  }

  /**
   * Get approval request details
   */
  getApprovalRequest(approval_id: string): ApprovalRequest | null {
    return this.approvalWorkflows.get(approval_id) || null;
  }

  /**
   * Determine if a mapping change requires approval (§48)
   */
  requiresApproval(mapping: {
    mapping_type: string;
    authority: string;
    status: string;
  }): 'four_eyes' | null {
    // Critical mappings requiring approval
    const criticalTypes = [
      'ACCOUNTING', // Financial postings
      'TAX', // Tax configuration
      'PAYMENT', // Payment routing
      'MIGRATION', // Data migration
    ];

    if (criticalTypes.includes(mapping.mapping_type)) {
      return 'four_eyes';
    }

    // Cross-tenant mappings always require approval
    // This would be detected by the presence of cross-tenant fields

    return null;
  }

  /**
   * Verify approval is complete and valid
   */
  verifyApprovalComplete(approval_id: string): boolean {
    const approval = this.getApprovalRequest(approval_id);
    if (!approval) {
      return false;
    }

    return approval.status === 'approved' && approval.approvals.length >= approval.required_approvers;
  }

  /**
   * Helper: compute field-level changes
   */
  private computeChanges(previous: any, current: any): Record<string, { from: any; to: any }> | undefined {
    if (!previous || !current) {
      return undefined;
    }

    const changes: Record<string, { from: any; to: any }> = {};

    const allKeys = new Set([...Object.keys(previous), ...Object.keys(current)]);

    for (const key of allKeys) {
      if (previous[key] !== current[key]) {
        changes[key] = {
          from: previous[key],
          to: current[key],
        };
      }
    }

    return Object.keys(changes).length > 0 ? changes : undefined;
  }

  /**
   * Helper: generate short random ID
   */
  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }
}

/**
 * Audit middleware helper for Express/HTTP frameworks
 *
 * Captures request context for audit trail
 */
export function createAuditContext(req: any): AuditContext {
  return {
    tenant_id: req.user?.tenant_id || 'unknown',
    actor_id: req.user?.subject || 'anonymous',
    actor_type: req.user?.actor_type || 'user',
    request_id: req.headers['x-request-id'] || `req_${Date.now()}`,
    correlation_id: req.headers['x-correlation-id'] || uuidv4(),
    causation_id: req.headers['x-causation-id'],
    origin: req.ip || req.connection.remoteAddress,
    http_method: req.method,
    http_path: req.path,
  };
}

/**
 * Factory for creating audit manager
 */
export function createAuditTrailManager(): AuditTrailManager {
  return new AuditTrailManager();
}
