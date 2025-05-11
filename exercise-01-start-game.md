# Exercise 1 [Start game]

- **Length:** 20-30 minutes

---

## 1.1. Introduction

In this exercise, we're going to implement the first part of the game: starting
a game. To make this a bit easier, we've provided you with stub files for this
exercise in `connect_four/exersize_01/`.

<details>
  <summary><i>Check your progress with the Connect Four CLI!</i></summary>

> To make the game more exciting, we've implemented a CLI-client that allows you
> to play a game of Connect Four. That is, if you manage to implement the
> necessary commands and events.
>
> You can run the game at any time by executing the following command, but note
> that the game will crash if you haven't implemented the necessary parts of the
> game yet:
>
> ```shell
> poetry run python -m connect_four.exercise_01.cli
> ```
</details>

<details>
  <summary><i>Running unit tests to check your progress</i></summary>

> Of course, another way to check your progress is by writing unit tests. We've
> provided you with an example test in `tests/test_game.py` to illustrate how
> you could write tests for your game. **This test will initially fail.**
>
> Feel free to add tests or alter the existing ones to check your progress. If
> you want, you can use Test-Driven Development (TDD) to implement the game.
>
> You can run the test suite by running:
>
> ```shell
> poetry run pytest tests/exercise_01
> ```
</details>


<br>

---

## 1.2. Initializing the aggregate

- Open the file `connect_four/exercise_01/domain/game.py`. This file contains a
  stub of the `Game` aggregate that is the model for a game of Connect Four.

- Write an `__init__`-method for the `Game` aggregate that sets two attributes,
  `player_one` and `player_two`. As the game has not started yet, you don't
  have player names yet. Assign a reasonable default that indicates the absence
  of a value (i.e., don't introduce parameters for the player names).

*Note: You may or may not like this design decision, but it's made for
educational purposes. (Isn't it nice how easy it is to rationalise design
decisions?)*

<br>

---

## 1.3. Starting a game with two players

To start a `Game`, the class needs to support a "Start Game"-command.

- Add a method, `start_game`, that starts a game by assigning the names of the
  two players to the relevant attributes initialized in `__init__`. The method
  should take two parameters, one for each name.

<br>

---

## 1.4. An eventful state of being

You may have noticed that we're currently still relying on state. This is not
what we want in an event-sourced system. Instead of manipulating state, we want
to record the events that alter the state.

- Add an attribute, `events`, to the `Game` class that will hold the events of
  the game in a `list`. Think of a place to _initialize_ this attribute with
  an empty list.

<br>

---

## 1.5. Not only elephants have memory

Now that we have a list to store the events, we want to "emit" and track a
`GameStarted`-event instead of manipulating state.

- Remove the assignment of players names in the `start_game`-method. That's
  right, we're not going to simply manipulate the `Game`-state.

We still need to keep track of the player names in *some* way now that you've
removed the assignments in the `start_game` method. The key insight here is that
the information is associated with the event: *We are starting a game between
two specific players.*

This means that the only way to keep track of the player names is by attaching
the relevant information to the event.

- Open `connect_four/domain/events.py` and look at the stub for the
  `GameStarted` event.


- Write an `__init__`-method for the `GameStarted` event that takes two
  parameters, `player_one` and `player_two`, and assigns them to the relevant
  attributes.


- **Optional:** If you have experience with `attrs` or `dataclasses`, use either
  to make instances of the event frozen/pseudo-immutable. The idea is that once
  an event has happened, it has happened and you can't do anything about it
  (unless you happen to be a time traveller).


- Now go back to the `start_game`-method and ensure that it instantiates a
  `GameStarted`-event containing the right information. Append it to `events`
  list you added above to ensure that you don't forget about this event!

<br>

> [!NOTE]
> Normally, you'd store something that is guaranteed to uniquely identify the
> players (e.g., a user ID) rather than the player names. However, for the sake
> of simplicity, we're using the player names as identifiers in this tutorial.
>
> Some of the code provided in this repository will use the player names for
> comparisons. This only works well if you use unique player names, especially
> later on in the tutorial.

<br>

---

## 1.6. Those who remember the past are able to repeat it

Congratulations, you've successfully persisted your information in an event
instead of the state of the object. However, it's still very handy to have easy
access to the current state while the `Game`-object is in memory. This is why we
want to *apply* the event to the `Game` state.

- Write an `apply`-method that applies the `GameStarted` event to the `Game`
  instance. In this case, this means that we want to assign the names of the
  players stored in the event to the relevant attributes of the `Game`
  instance.


- Call the `apply`-method from the end of the `start_game`-method to ensure
  that this command has the expected effect on the game state. If you don't,
  the event history and the game state will be out-of-sync...

The steps above may feel a bit weird, but if you think about it, the state of
the `Game` now reflects that the event has happened. Moreover, if you were to
persist the **event** (not the state of the `Game`!), you can now use this
`apply`-method on a "fresh" instance of `Game` to recreate a `Game`-instance
with the exact same state as you have right now.

This is the magic of Event Sourcing: You *replay the events* to recreate the
state of the aggregate rather than persisting the state itself.

<br>

---

## 1.6. Play the game

You can try the game in the console:

```shell
poetry run python -m connect_four.exercise_01.cli
```

If you didn't finish your implementation, but still want to play, you can use
the CLI from the solution for that:

```bash
cd .internal/solutions
poetry run python -m connect_four_solutions.exercise_01.cli
```

<br>

---

## Bonus exercise: Constraints are the best thing since sliced bread

What should happen if you issue a `start_game`-command for the second time on
the same game? Implement a solution for this potential problem.

Hint: Can you think of a *constraint* that would prevent a second command from
creating a second `GameStarted`-event?

<br><br>

---

<p align="center">
   <a href="/README.md">⬅️ Back to the README</a> | <a href="/exercise-02-play-the-game.md">Continue to exercise 2 ➡️</a>
</p>
