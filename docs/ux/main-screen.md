# Main Screen UX

## Purpose

The main screen is the primary interaction surface of Time Grinder.

Its purpose is to let the user quickly record and understand how time is being
distributed between Projects.

The screen is designed mobile-first and should be comfortable to use with one
hand.

The main screen is not a project-management screen.

Users do not navigate into Project detail pages from the main screen in the
MVP.


## Main screen elements

The main screen contains:

- Project cards / containers
- quick-add time bubbles
- Start / Stop timer control
- currently running timer
- Undo last action control
- application menu

Projects are the main visual elements of the screen.

Each Project represents a container receiving time.


## Project cards

Each Project is displayed as a large touch-friendly visual container.

A Project card shows:

- Project name
- total tracked time for Today

Example:

```text
┌─────────────┐
│    Baby     │
│             │
│    2h 15m   │
└─────────────┘
```

Project cards are not clickable for navigation in the MVP.

There is no Project details screen accessible from the main screen.

## Quick time bubbles

The MVP contains fixed quick-add time values:

+15 min
+30 min
+1 hour

These values are not configurable in the MVP.

A time bubble is a draggable visual object representing a fixed amount of time.

Example:

+15m
  ●

The user can drag a time bubble onto a Project card.

Dropping the bubble onto a Project immediately creates and saves an Action.

No confirmation dialog is shown.

## Quick-add flow

Example:

User picks up a +30 min bubble.
User drags it onto the Baby Project.
User releases the bubble.
A 30-minute Action is immediately saved for Baby.
The Project's Today total is updated.
Undo becomes available.

```text
+30m
        ●
        │
        │ drag
        ▼

┌─────────────┐
│    Baby     │
│             │
│    2h 15m   │
└─────────────┘
```

after dropping:

```text
┌─────────────┐
│    Baby     │
│             │
│    2h 45m   │
└─────────────┘
```

## Action creation

A quick-add drop creates an Action immediately.

The Action contains at least:

Project
duration
timestamp / time information required by the domain model

No description is required.

Saving should feel immediate.

The UI should update optimistically where practical, but failed persistence must
not silently lose data.

## Timer

Only one timer can run at a time in the MVP.

The user selects a Project and starts the timer.

While the timer is running:

the active Project is clearly visible;
elapsed time is displayed on the main screen;
changing to another Project is disabled;
starting another Project timer is disabled;
quick-add interaction may remain available unless later UX testing shows this
is confusing.

The user must stop the current timer before another Project can become the active
timer Project.

## Starting a timer

Initial flow:

User selects a Project.
User presses Start.
The Project becomes the active Project.
Timer begins.
Project switching controls become disabled.
Elapsed time is visible on the main screen.

## Running timer state

The running timer must be visible without opening another screen.

Example:

```text
Running

Work
00:43:17
```

The exact visual placement is not fixed yet.

The active Project should be visually distinguishable from other Projects.

## Project switching while timer is running

In the MVP, Project switching is blocked while the timer is running.

The application must not automatically stop the current Project and start
another one.

If the user wants to track another Project:

stop the current timer;
select another Project;
start a new timer.

Controls that would change the active timer Project should be visually disabled
while a timer is running.

## Stopping a timer

When the user presses Stop:

the timer stops;
an Action is created for the active Project;
the Action is saved immediately;
the Project's Today total is updated;
Project selection becomes available again;
Undo becomes available.

## Undo

Undo reverses the most recent time-recording action.

The MVP supports only undoing the latest operation.

Examples of undoable operations:

adding +15 min to a Project;
adding +30 min to a Project;
adding +1 hour to a Project;
stopping a timer and creating its Action.

Undo does not open an action history.

Undo should be easy to reach from the main screen.

The initial design places Undo / Cancel-last-action near the top-left corner.

## Today totals

Each Project displays tracked time for the current day.

The MVP does not show weekly or monthly totals on the main screen.

Example:

Work
4h 35m

Baby
2h 10m

Sleep
7h 20m

The purpose is to give the user a quick visual understanding of where today's
time has gone.

## Main screen interaction states

The screen has at least three important states.

### Idle

No timer is running.

The user can:

select a Project;
start a timer;
drag quick-add time onto Projects;
undo the last action, if available;
open the menu.

### Running

A timer is running.

The user can:

see the active Project;
see elapsed time;
stop the timer;
undo a previous action if the product allows it safely during an active timer;
open the menu.

The user cannot:

switch the timer to another Project;
start another timer.

### Dragging time

A quick-add bubble is being dragged.

The UI should make valid Project drop targets visually obvious.

The interaction should feel direct and physical.

Releasing the bubble over a valid Project immediately saves the Action.

## Error handling

The product should avoid confirmation dialogs for normal time entry.

If an Action cannot be saved:

the UI must clearly indicate failure;
the Project total must not remain permanently incorrect;
the user should be able to retry.

Network or persistence errors should not result in silent data loss.


## UX principles
The main screen should follow these principles:

Time entry is faster than opening a form.
Important controls are reachable with one hand.
Projects are large touch targets.
Actions happen immediately.
Mistakes are corrected through Undo rather than confirmation dialogs.
Running timer state is always obvious.
The user should understand today's time distribution at a glance.

## Out of scope for MVP

The main screen does not include:

Project editing
Area editing
Project detail pages
configurable quick-add durations
multiple simultaneous timers
automatic Project switching
complex reports
calendar views
goals or quotas
productivity scoring
