# Track: Transfer & timer task processing

slug: task-processing
days: 20
repos: server=cadence-workflow/cadence, client=cadence-workflow/cadence-go-client
status: curated

20 days, 10-15 minutes each, from fundamentals to edge cases. Day 0 (first invocation of this track) generates `syllabus.md` in the track's course dir following this arc. The generated syllabus assigns each day ONE topic, 2-4 anchor files (real paths in the server or go-client repo), and a one-line exercise idea. The user may edit `syllabus.md` by hand at any time; the skill always reads it fresh.

## The arc

### Week 1 (days 1-5): fundamentals

1. Why background tasks exist: workflow state transitions must atomically schedule follow-up work. Transfer vs timer tasks at a glance. History service and shards in one page.
2. Where tasks are born: the mutable state task generator (`service/history/execution/mutable_state_task_generator.go`) and the task structs (`common/persistence/tasks.go`).
3. How tasks are persisted: the executions store, transfer/timer task categories (`common/persistence/tasks.go` `HistoryTaskCategory`, `common/persistence/task_manager.go`, `data_store_interfaces.go`), task IDs vs visibility timestamps (immediate vs scheduled queues).
4. Queue processor architecture overview: `service/history/queue/`, task fetching, processing queue states, per-shard processors.
5. Task lifecycle end-to-end: create → read → filter → execute → ack / complete → range-complete; task executor interfaces (`service/history/task/`).

### Week 2 (days 6-10): transfer tasks in depth

6. Transfer task type tour: ActivityTask, DecisionTask, CloseExecution, CancelExecution, SignalExecution, StartChildExecution, RecordWorkflowStarted (`common/persistence/tasks.go`, `service/history/task/transfer_active_task_executor.go`).
7. ActivityTask + DecisionTask: handoff to matching — what the history service pushes, what matching enqueues (`client/matching`, `service/matching/`).
8. Go-client side: poller loops, task handlers, RespondActivityTaskCompleted / RespondDecisionTaskCompleted closing the loop (client repo: `internal/internal_task_pollers.go`, `internal/internal_worker.go`).
9. CloseExecution: everything that happens when a workflow closes — visibility records, parent notification, child policy (`transfer_active_task_executor.go`).
10. Cancel/Signal/StartChild transfer tasks: cross-workflow RPCs, retries and the "recorded" pattern in mutable state.

### Week 3 (days 11-15): timer tasks in depth

11. Timer task type tour: UserTimer, ActivityTimeout, DecisionTimeout, WorkflowTimeout, ActivityRetryTimer, WorkflowBackoffTimer, DeleteHistoryEvent (`common/persistence/tasks.go`, `service/history/task/timer_active_task_executor.go`).
12. The timer sequence: how mutable state tracks pending timers and only persists the nearest one (`service/history/execution/timer_sequence.go`).
13. Activity timeouts in detail: ScheduleToStart / ScheduleToClose / StartToClose / Heartbeat; heartbeat resets and their timer churn.
14. The timer queue: lookahead, redispatch of not-yet-fireable tasks, ack manager for a time-ordered queue (`service/history/queue/timer_queue_processor_base.go` and sibling `timer_queue_*.go`, `service/history/task/redispatcher.go`).
15. Timer fires → history events → new tasks: the full cascade (for example, an activity timeout produces a DecisionTask transfer task).

### Week 4 (days 16-20): nitty-gritty edge cases

16. Shard movement: what happens to in-flight tasks when a shard moves; rangeID fencing, task re-reading from ack level, at-least-once semantics.
17. Ack levels, retries, redispatch, and DLQ: what advances the ack level, what blocks it, when a task is retried forever vs dropped (`service/history/queue/`, task DLQ work).
18. Stale-task races: timer fires after activity completed, task for a deleted/reset workflow, version/eventID checks that make executors idempotent (`verifyTaskVersion`, load-check patterns in executors).
19. Active vs standby processing: what a standby cluster does with transfer/timer tasks, resend/redispatch on missing events (`service/history/task/transfer_standby_task_executor.go`, `timer_standby_task_executor.go`, `standby_task_util.go`).
20. Failover and reset interplay: domain failover mid-task, reset creating a new run while old-run tasks still exist; graceful failover markers. Wrap-up plus final cumulative quiz.

## syllabus.md format

```markdown
# <track title> — <N>-day course

## Day NN: <topic title>
- **Goal**: <one sentence>
- **Anchors**: <2-4 repo-relative file paths, verified to exist>
- **Exercise idea**: <one line, a 5-10 line simplified implementation>
- **Builds on**: day(s) <...>
```

Anchor paths MUST be verified with `ls`/`grep` against the repos before the syllabus is finalized — file names above are starting hints, not gospel; the repos evolve.
