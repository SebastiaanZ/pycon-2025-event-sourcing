# Exercise 2 [Play the game]

- **Length:** 30 minutes

<br>

---

### 2.1. Introduction

Now we can start a game, it's time to implement the rest of it. By the end of
this exercise, you'll have a working game that you can play using the console
interface we've provided. Obviously, this will only work properly once you've
implemented the missing parts of the game.

Note that you won't continue with your own solution to exercise one. While this
would have been fun, we've added some helper code and game logic that ensures
we can focus on the Event Sourcing part of the implementation.

<details>
  <summary><i>Playing Connect Four in your Console</i></summary>

> You can run the console client for Exercise 02 using the following command:
>
> ```shell
> poetry run python -m connect_four.exercise_02.cli
> ```
>
> This CLI-client may behave unexpected or crash until you've implemented all
> parts of this exercise.
</details>

<details>
  <summary><i>Unit Tests as your Guide</i></summary>

> We've provided some unit tests for this exercise in the test module
> [`tests/exercise_02/test_game.py`](tests/exercise_02/test_game.py). The first
> two tests should pass as-is, but the third will fail until you've implemented
> the part that allows players to make moves.
>
> You can run these tests with:
>
> ```shell
> poetry run pytest tests/exercise_02
> ```
>
> Feel free to add test cases of your own during your development process.
</details>


<br>

---

### 2.2. You've got to move it, move it

A game is no fun if you can't make moves. That's why we're going to add support
for player moves to our game of Connect Four.

Since we're focusing on the event sourcing aspect today, we're not going to
implement the game logic. Instead, we're going to use a `Board`-class that
handles the game logic for us.

The `Board`-class tracks the state of the board, has methods for checking if a
column is full, and has a method for checking if the game has ended. However, it
does not know anything about the players or the game itself. Each instance of
the `Game`-class automatically creates a `Board`-instance.

**You won't have to change the `Board`-class yourself, but you will need to
use it.**

Note: The first player uses yellow tokens in this game, while the second player
uses red tokens. There's an enum in `src/connect_four/domain/enums.py` for this.

- Write the implementation for the `make_move`-method. This command should
  instantiate a `MoveMade`-event and use the `_process_event`-method to apply
  the event to the aggregate and append it the `events` list. You should also
  add support for this event in the `Game.apply`-method to update the state of
  the `Game`-aggregate.

- You may have noticed that the new version of `Game` also has a `next_player`
  attribute. Ensure that it's always filled with the name of the player who's
  next. Don't forget to set `next_player` before the first move is made!

> [!TIP]
> Think about the data that you need to store in the event, but also think about
> the state of the `Game` instance that you need to update. In particular, our
> clients need to be able to ask for the _next player_ using the attribute
> `Game.next_player`.
>
> However, is it necessary to store that information as part of the event?

> [!IMPORTANT]
> For this implementation, only update the state of the `Game`-aggregate in
> the `apply`-method. The `make_move`-method should only be responsible for
> instantiating the event and emitting it.
>
> The reason why we're doing this will become clear in the next exercise, but
> it has to do with being able to both apply historical events and new,
> uncommitted events to the aggregate.
>
> However, it's likely that you want to solve this in some other way in an
> actual "production-ready" implementation of Event Sourcing. Current Python
> frameworks for Event Sourcing typically use a bit of meta-programming
> decorator magic for this.

<br>

---

### 2.3. It's getting crowded in here

Making moves is great, but we need to be careful that players don't make moves
that are not allowed. One such constraint is "For a player to make a move in a
specific column, that column **must** have room for another token."

- Add a constraint to the `make_move`-method that prevents a player from
   placing a token in a column that's already full.

> [!TIP]
> The `Board`-class already provides a `has_room_in_column`-method that you can
> use to perform the check.

<br>

---

### 2.4. The end is nigh

Now you can make moves. There's just one problem: This game will never end. Once
the board is full, every move you try to make will be rejected by the constraint
you just implemented but the game still won't end.

That's why you're going to get us out of this infinite game by implementing a
`GameFinished`-event.

- Add a `GameFinished`-event and add attributes for the information you think it
  should contain.

<details>
  <summary><i>Hint: What Information Do You Need To Store?</i></summary>

> Remember that we're never going to persist the state of an aggregate as-is,
> only the events that determined the state. This means that if you want to
> store the result of a game. you have to associate that information with the
> event.
>
> How you store that information is a design choice. The game already "knows"
> who the players are, so you might just store "player a won", "player b won",
> or "game ended in a draw".
</details>

How will this event ever be triggered? In our case, this event is simply an
event that *sometimes* follows a `MoveMade`-event.

- Check if a game has ended right after the `MoveMade`-event in the `make_move`
  command. If it has ended, emit a `GameFinished`-event. **Note:** the `Board`
  class has a `get_result`-method that you can use to check if the game has
  finished.

<br>

> [!IMPORTANT]
> Don't forget to apply the event to the `Game`-aggregate!

<br>

---

### 2.5. All work and no play makes Jack a dull boy

Use the CLI to beat another tutorial participant with the game you just
implemented.

```shell
poetry run python -m connect_four.exercise_02.cli
```

If you didn't finish your implementation, but still want to play, you can use
the CLI from the solution for that:

```shell
cd .internal/solutions
poetry run python -m connect_four_solutions.exercise_02.cli
```

<br>

---

### 2.5. Bonus exercise: Constraints are the best thing since sliced bread

Should you be able to make moves before the game has started? What about after
it's ended? And what should happen if player one tries to make two moves in a
row to beat player two?

- Add additional constraints to `make_move` to prevent these shenanigans.

<br><br>

---

<p align="center">
   <a href="/exercise-01-start-game.md">⬅️ Back to exercise 1</a> | <a href="/exercise-03-persist-the-events.md">Continue to exercise 3 ➡️</a>
</p>
