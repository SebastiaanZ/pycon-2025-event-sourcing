# Exercise 3 [Persist the events]

- **Length:** 30-40 minutes

All that buzz about persisting events instead of state, and we haven't even
persisted anything yet. Let's change that.

## 3.1. In-Memory Store vs KurrentDB Container

There are two options for this exercise: You can either run a container with
KurrentDB, a database optimized for Event Sourcing, or use an in-memory event
store that emulates the tiny bit of KurrentDB that we need.

If you haven't pre-pulled the docker image before this tutorial, you may not be
able to do so now due to limited network conditions at the venue. In that case,
I'd recommend using the in-memory event store.

The choice **doesn't influence the code that you have to write**, but talking to
the real thing may be more fun.

_Note that the in-memory client does not persist any data between runs._

### 3.1.1. Using the in-memory version

By default, the CLI-interface that we provide and the test fixture that we wrote
will use the in-memory event store. This means that if you want to use the
in-memory version, you don't have to do anything special while running the game
or tests:

```bash
poetry run python -m connect_four.exercise_03.cli
```

```bash
poetry run pytest tests/exercise_03
```

If you want to create your own instance of the `GameRepository`, you can create
it like this to use the in-memory version:

```python
from connect_four import helpers
from connect_four.exercise_03 import persistence

client = helpers.InMemoryEventStoreClient()
repo = persistence.GameRepository(client=client)
```

### 3.1.1. Using KurrentDB

If you want to use KurrentDB, you can run one of following command from the root
directory of the repository to start a container:

- For podman, use:

```bash
podman run --rm -it --name kurrentdb -p 2113:2113 --env-file=.kurrentdb.env docker.kurrent.io/kurrent-latest/kurrentdb:latest
```

- For docker, use:

```bash
docker run --rm -it --name kurrentdb -p 2113:2113 --env-file=.kurrentdb.env docker.kurrent.io/kurrent-latest/kurrentdb:latest
```

This will start a docker container with KurrentDB that you can stop by pressing
"ctrl + c". Once you stop the container, all data will be lost. This makes it
easy to reset the state of the database if you want to.

To run the CLI or tests with KurrentDB, you can add the `--use-kurrentdb` flag
to the commands:

```bash
poetry run python -m connect_four.exercise_03.cli --use-kurrentdb
```

```bash
poetry run pytest --use-kurrentdb tests/exercise_03
```

If you want to create your own instance of the `GameRepository`, you can create
it like this:

```python
from connect_four.exercise_03 import persistence

import kurrentdbclient

client = kurrentdbclient.KurrentDBClient("kdb://localhost:2113?tls=false")
repo = persistence.GameRepository(client=client)
```

> [!TIP]
> KurrentDB provides a web interface to inspect streams. You can access it at
> http://localhost:2113/web/index.html#/streams.

---

## 3.2. Exploring the repoverse

In the following exercises, you'll implement a `GameRepository` that persists
events in an Event Store and retrieves them.

We've provided a minimal application layer to make connecting the dots a bit
easier. You won't have to touch this layer, but it does contain an interface
that our `GameRepository` has to implement.

You can find there relevant files in [
`/src/connect_four/exercise_03/application/`][application-directory].

This application layer is used by the CLI-interface that you can use to play the
game. (For instructions on how to run the CLI-interface, see section 3.1.)

In addition to the application layer, we've also provided you with a stub for
the `GameRepository`.

1. Check out the stub in [
   `src/connect_four/exercise_03/persistence/`][esdb-game-repository]

<br>

<details>
  <summary><i>Writing tests for the repository</i></summary>

> The `GameRepository` expects an instance of an Event Store client to
> interact with the Event Store. This allows us to inject either the in-memory
> client or the KurrentDB client:
>
> ```python
> import kurrentdbclient
>   
> from connect_four.exercise_03 import persistence
> from connect_four import helpers
>
> in_memory_client = helpers.InMemoryEventStoreClient()
> repo_in_memory = persistence.GameRepository(client=in_memory_client)
> 
> kurrentdb_client = kurrentdbclient.KurrentDBClient("esdb://localhost:2113?tls=false")
> repo_kurrentdb = persistence.GameRepository(client=kurrentdb_client)
> ```
>
> To make this easer, we've provided a test fixture that will determine which
> client to use based on the command line arguments you pass to `pytest`. If you
> run `pytest` with `--use-kurrentdb`, it will use the KurrentDB client. If not,
> it will use the in-memory client.
>
> See the examples
> in [tests/exercise_03/test_game_repository.py](tests/exercise_03/test_game_repository.py)
> for examples on how to use this fixture.


> [!IMPORTANT]
> KurrentDB is designed to be immutable. There are no easy ways to "clean" or
> "remove" streams or events from the database. This means that if you run your
> test suite multiple times, the events will accumulate in the database.
>
> As our game streams will use Game IDs in their names, which is a random UUIDs,
> this shouldn't cause too many issues for this tutorial.
>
> If you want to write integration tests for actual projects, you could consider
> using a test container that you restart between tests or test runs. For unit
> tests, you can [inject][there-is-nothing-difficult-about-this] a test double.
</details>

[there-is-nothing-difficult-about-this]: https://www.youtube.com/clip/Ugkxk8enfYMInruaxQWXb90kVF3J9Jivgs9n

[application-directory]: /connect_four/exercise_03/application/

[esdb-game-repository]:  /connect_four/exercise_03/persistence/game_repository.py

<br>

---

## 3.3. If a game starts in the forest...

If a game starts in the forest and there's no repo to store the event, did it
truly start? Since we only store events, not state, the only way to save a game
is by storing its events in an event store.

That's why the `start_game`-method of the application service creates a `Game`,
executes the `start_game`-command on the game, and then persists the events of
the game to the event store using the repository.

In this exercise, you will implement the persistence logic required to make the
`GameRepository.add`-method store the events of a `Game` in EventStoreDB.

<br>

<details>
  <summary><i>Quick Example of Using the EventStoreDBClient</i></summary>

> Here's an example that appends events to a stream using the `KurrentDBClient`:
>
> ```python
> import kurrentdbclient
> 
> from connect_four import helpers
>
> # You'll need to translate events to esdbclient events:
> event1 = kurrentdbclient.NewEvent(type='ThingHappened', data=b'{"data":"bytes"}')
>   
> # And have a name for the event stream
> stream_name = "some-event-stream-name"
>   
> # Now you can append the NewEvent to the stream (in-memory version)
> client_in_memory = helpers.InMemoryEventStoreClient()
> client_in_memory.append_to_stream(
>     stream_name=stream_name,
>     current_version=kurrentdbclient.StreamState.ANY,
>     events=[event1]
> )
>   
> # Now you can append the NewEvent to the stream (KurrentDB version)
> client_kdb = kurrentdbclient.KurrentDBClient("esdb://localhost:2113?tls=false")
> client_kdb.append_to_stream(
>     stream_name=stream_name,
>     current_version=kurrentdbclient.StreamState.ANY,
>     events=[event1]
> )
> ```
</details>

<br>

1. Add an implementation to `GameRepository.add` that persist a`Game` with only
   a `GameStarted`-event.

   This requires a few steps:
    1. Map a domain event to an `esdbclient.NewEvent`. Use `GameStarted` as the
       event type and serialize the event data to a JSON string using the
       `json.dumps`. You do need to encode the string to bytes with
       `str.encode("utf-8")`
    2. Determine the stream name based on the game ID using `f"game-{game.id}"`.
    3. Append the event to the stream using `self._client.append_to_stream`.

<br>

> [!TIP]
> There's a test in `tests/exercise_03/persistence/test_game_repository.py` that
> you can use
> to test your implementation.

<br>

---

## 3.4. Now... where was I?

Having a great memory is no use if you can't retrieve anything. So, let's add
retrieval logic to the `GameRepository`.

<br>

<details>
  <summary><i>Quick Example of Retrieving Events</i></summary>

> Retrieving events from a stream is fairly straightforward:
>
> ```python
> # In-memory version
> from connect_four import helpers
> 
> client = helpers.InMemoryEventStoreClient()
> recorded_events = client.get_stream("stream-name-here")
> ```
>
> ```python
> # KurrentDB version
> import kurrentdbclient
> 
> client = kurrentdbclient.KurrentDBClient("esdb://localhost:2113?tls=false")
> recorded_events = client.get_stream("stream-name-here")
> ```
>
> The `EventStoreDBClient.get_stream`-method will return a `tuple` with
> `RecordedEvent`-objects. Like `NewEvent`-objects, `RecordedEvent`-objects have
> a `type` and `data` attribute that you can use to recreate the domain event
> you stored.
</details>

<br>

1. Add logic to the `get`-method that retrieves the events in the game stream
   using `self._client.get_stream`.

2. Write logic to map the `RecordedEvent` to the domain event `GameStarted` and
   apply it to the events you received from the stream.

4. Look at the classmethod `load_from_history` of the `Game`-class. Its purpose
   is to create a new `Game` with the specified `id` and a reconstructed state
   by applying the historical events. Implement this method.
    - _Don't forget to add the historical events to events list!_

5. Now use this method in the repository's `get`-method with the events
   resurrected from the event store.

6. Now that you've recreated the `Game`-instance in the correct state, return
   it to the caller.

<br>

> [!TIP]
> There's a test in `tests/exercise_03/persistence/test_game_repository.py` that
> you can use
> to test your implementation. (You do have to remove the skip decorator.)

<br>

---

## 3.5. Show Me Your Moves

1. Now add support for persisting and retrieving `MoveMade` events by adding the
   mapping logic for this event to both mapping functions.

2. Remove the `skip` from the `test_game_repository_stores_move_made_events`
   test in `tests/persistence/test_game_repository.py` and notice that **it
   still fails when you run it!**

   As you can see, we've appended three rather than two events to the event
   stream. What's going on here?

<br>

---

### 3.6. Those who include history are forced to repeat it

The problem is that when the events of the `Game`-instance were persisted after
the move was made, the `Game.events` list contained two events: `GameStarted`
and `MoveMade`.

Since we are *appending* events to the event and the `GameStarted` event was
already stored when the game was created, persisting the entire `Game.events`
list will store another `GameStarted` event!

*This is obviously a problem.*

How would you solve this? Keep in mind that the `Game`-instance would be out of
sync if you were to omit historic events entirely. This is problematic because
we do want to be able to check constraints and perform other business logic that
relies on the historical events.

<br><br>

One solution to this problem is to separate the historical events from the
uncommitted events. This is the solution that we're going to implement here.

1. Replace the `events`-attribute of the `Game`-class with two attributes:
   `historical_events` and `uncommitted_events`.

2. Change the `load_from_history`-method to store the historical events in the
   `historical_events`-attribute.

3. Change the `process_event`-method so that it appends new events to the
   `uncommitted_events`-attribute.

4. Add a property, `events`, that returns the concatenation of the
   `historical_events` and `uncommitted_events`-attributes. Make sure to retain
   the proper order of events in the concatenation.

5. Change the `GameRepository.add`-method to store the `uncommitted_events` in
   the event stream instead of all the events.

6. Check if this solved the problem by rerunning the test from the previous
   exercise.

<br>

---

## 3.7. The end is nigh (of the workshop, not the game...)

Now add support for persisting and retrieving `GameFinished` events.

<br>

## 3.8. Connect Four: The Final Battle

That should be it. You've successfully implemented an event-sourced Connect Four
game.

You can play your game using the CLI-client:

```shell
poetry run python -m connect_four.exercise_03.cli
```

```shell
poetry run python -m connect_four.exercise_03.cli --use-kurrentdb
```

You can also run the command-line interface from the solution:

```shell
cd .internal/solutions
poetry run python -m connect_four_solutions.exercise_03.cli
```

```shell
cd .internal/solutions
poetry run python -m connect_four_solutions.exercise_03.cli --use-kurrentdb
```

<br><br>

---

<p align="center">
   <a href="/exercise-02-play-the-game.md">⬅️ Back to exercise 2</a> | <a href="https://404-exercise-not-found.pycon-us">Continue to exercise 404 ➡️</a>
</p>
