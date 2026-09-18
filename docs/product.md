# Time Grinder — Product

## Vision

Time Grinder is a lightweight personal time-tracking application designed
 for mobile and desctop (web application) use.

Its goal is not precise work-time accounting.

The goal is to help a person quickly understand:

- where their time goes;
- which parts of life receive enough attention;
- which projects are being neglected;
- how time is distributed between different areas of life.

The core interaction should be fast enough to use casually throughout the day,
ideally with one hand on a phone.

Time should feel like something the user distributes between projects rather
than something they need to carefully log into a timesheet.


## Product principle

Tracking time must require as little attention as possible.

The application should favor:

- large touch targets;
- visual interactions;
- approximate time entry;
- one-handed mobile usage;
- fast undo;
- minimal text input.

The product should avoid requiring the user to fill forms every time they want
to record time.


## Core domain model

### Area

An Area represents a broad part of life.

Examples:

- Health
- Self Improvement
- Family
- Adulting
- Recreation


### Project

A Project represents something inside an Area that receives time. These are where we put our time.

Examples:

Health:
- Sport
- Sleep

Family:
- Baby
- Wife Time

Adulting:
- Work
- Chores

Recreation:
- Games
- Chill

Self Improvement:
- Write Games
- Write Programs


### Action

An Action represents tracked time assigned to a Project.

Every Action:

- belongs to a Project;
- has a non-null amount of time;
- may optionally contain information about what the user did;
- can be created automatically by a timer;
- can be added manually;
- can be edited afterwards.

Possible conceptual model:

Action:
- id
- project_id
- started_at
- ended_at
- duration
- description (optional)
- created_at

An Action does not need a description.

Time is the only required meaningful value.


## Main interaction model

The main screen represents Projects visually.

Projects should feel like containers that accumulate time.

The user can track time in two main ways.


### Timer flow

1. User selects a Project.
2. User starts the timer.
3. User stops the timer.
4. An Action is created and assigned to that Project.


### Manual time flow

The user can create a block/bubble representing an amount of time.

Examples:

- +15 min
- +30 min
- +1 hour

The user can drag the time bubble onto a Project.

Dropping the bubble on a Project creates an Action for that amount of time.

The interaction should feel similar to putting a physical object into a
container.


## Drag interaction

Time can be represented as draggable visual objects.

Example:

A "+30 min" bubble can be picked up with a finger and dragged onto the
"Baby" Project.

After dropping:

- 30 minutes are added to Baby;
- an Action is created;
- the UI immediately reflects the change.

If the user made a mistake, they should be able to quickly undo the action.

Undo is preferred over confirmation dialogs.

The product should generally follow the rule:

> act first, undo easily

rather than:

> confirm every action before doing it


## Main mobile screen

The main screen should contain:

- Projects represented as large touch-friendly visual containers;
- quick time bubbles such as +15 min and +1 hour;
- a prominent Start / Stop timer control;
- an Undo / Cancel-last-action control;
- access to the application menu.

The screen should be usable comfortably with one hand.

Precise layout is not yet fixed.

The initial concept includes:

- Undo in the top-left;
- Menu in the top-right;
- Project containers in the main area;
- Quick-add time bubbles near Projects;
- Start / Stop control near the bottom.


## Reports

The MVP requires one primary report:

Time spent by Project.

The user should be able to understand how much time was spent on each Project
during a selected period.

Initial useful periods:

- Today
- This week

More complex analytics are explicitly not required for the MVP.


## MVP

The first version should allow a user to:

- see predefined Areas;
- see predefined Projects;
- start tracking time for a Project;
- stop the running timer;
- manually add time to a Project;
- create an Action from manually added time;
- edit an Action;
- view a list of Actions;
- undo the most recent time entry;
- see time spent by Project;
- use the application comfortably from a mobile-sized screen.


## Default Areas and Projects

### Health

- Sport
- Sleep

### Self Improvement

- Write Games
- Write Programs

### Family

- Baby
- Wife Time

### Adulting

- Work
- Chores

### Recreation

- Games
- Chill


## User model

The product should eventually support multiple users.

Each user's data must be isolated.

However, account management is not part of the MVP.

The initial implementation may use a minimal authentication mechanism or a
temporary simplified user model as long as the architecture does not assume
that only one user will ever exist.


## Non-goals for MVP

The following are explicitly outside the first version:

- custom Area editor;
- custom Project editor;
- complex account management;
- teams;
- shared projects;
- billing;
- productivity scoring;
- goals and quotas;
- notifications;
- calendar integration;
- complex charts;
- detailed analytics;
- automatic activity detection;
- desktop application;
- native mobile application.


## Platform

The long-term target is a mobile application.

Web application is also required.

The first implementation may be a responsive web application.

The UI and interaction model should therefore be designed mobile-first from the
beginning.


## UX priorities

In order of importance:

1. Very fast time entry.
2. Comfortable one-handed mobile use.
3. Low cognitive load.
4. Easy correction of mistakes.
5. Clear visual understanding of where time went.
6. Precise accounting.


## Product hypothesis

People often fail to track personal time because conventional time trackers
require too much deliberate interaction.

If recording time feels more like moving physical pieces between containers
than filling out a timesheet, users may track their day more consistently.

Time Grinder should test this hypothesis.