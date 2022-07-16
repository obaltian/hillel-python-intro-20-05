import asyncio
import itertools
import string
import threading
from multiprocessing.dummy import Pool

import aiohttp


def get_queries() -> list[str]:
    permutations = itertools.permutations(
        string.ascii_lowercase,
        r=3,
    )
    queries = ["".join(permutation) for permutation in permutations]
    return queries


async def get_hints(
    query: str,
    session: aiohttp.ClientSession,
) -> dict[str, list[str]]:
    print(f"get hints for {query}")
    response = await session.get(
        f"https://search.rozetka.com.ua/search/api/v6/autocomplete/"
        f"?front-type=xl&country=UA&lang=ru&text={query}",
    )
    print(f"got hints for {query}")
    response.raise_for_status()
    response_json = await response.json()
    try:
        hints_data = response_json["data"]["content"]["records"]["words_additions"]
    except:
        hints = []
    else:
        hints = [name for hint in hints_data if (name := hint.get("name"))]
    query_to_hints = {query: hints}
    return query_to_hints


def save_hints(
    hints: dict[str, list[str]],
    *,
    out: str = "hints.csv",
    sep: str = ",",
) -> str:
    with open(out, "w") as csv:
        csv.write(f"Query{sep}Hints\n")
        for query, hint_results in hints.items():
            hint_row = "; ".join(f"'{hint}'" for hint in hint_results)
            csv.write(f"'{query}'{sep}{hint_row}\n")
    return out


async def main() -> None:
    queries = get_queries()

    async with aiohttp.ClientSession() as session:
        async_tasks = (get_hints(query, session) for query in queries)
        query_to_hint_pairs = await asyncio.gather(*async_tasks)

    # query_to_hint_pairs = Pool(50).map(get_hints, queries)
    # query_to_hint_pairs = list(map(get_hints, queries))

    query_to_hints = {
        query: hints
        for pair in query_to_hint_pairs
        for query, hints in pair.items()
    }
    output = save_hints(query_to_hints)
    print(f"Saved hints to {output}")


if __name__ == "__main__":
    asyncio.run(main())


"""

1. Multiprocessing (different CPU cores)
    1. Hard to share variables (IPC - interprocess communication)
    2. For CPU-bound

2. Multitheading (OS threads) - one at time (GIL)
    1. Easy to share variables
    2. For IO-bound

3. Asynchronous programming



2 type of tasks: CPU-bound and IO-bound

Concurrency vs Parallelism vs Consecutive (последовательное исполнение)
"""
