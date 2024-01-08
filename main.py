"""
# NFA to DFA Converter.

This program converts a NFA to a DFA.

## Authors:
    - [Amir Mahdi Erfani Zadeh](amiwrpremium@gmail.com) --> 980122838
    - [Amir Hossein Roshannafs](amirhosinroshannafs@gmail.com) --> 962240751

## Date:
    - 2023-01-08 (January 08, 2023)
    - 1402-10-18 (18 Dey 1402)

## Usage:
    ```python main.py``` or ```python3 main.py```

## Repository
    - [GitHub](https://github.com/amiwrpremium/nfa_to_dfa)
"""

import typing as t
import time


def typing_effect(text: str, char_speed: float = 0.05, space_speed: float = 0.5):
    """
    Simulate typing effect.

    Args:
        text (str): Text to print.
        char_speed (float): Speed of each character.
        space_speed (float): Speed of space (and new line) characters.

    Returns:
        None.
    """

    for char in text:
        print(char, end="", flush=True)
        if char in ("", " ", "\n"):
            time.sleep(space_speed)
        else:
            time.sleep(char_speed)
    print()


class NotInAlphabetError(Exception):
    """
    Exception raised when a symbol is not in the alphabet of a DFA.
    """

    def __init__(self, symbol: str, alphabet: set):
        """
        Constructor.

        Args:
            symbol (str): Symbol that is not in the alphabet.
            alphabet (set): Alphabet of the DFA.
        """

        self.symbol = symbol
        self.alphabet = alphabet

    def __str__(self) -> str:
        """
        String representation of the exception.

        Returns:
            str: String representation of the exception.
        """

        return f"Symbol '{self.symbol}' not in alphabet {self.alphabet}"


class NFA:
    """
    Non-deterministic Finite Automaton.
    """

    def __init__(
            self,
            states: t.Set[str],
            alphabet: t.Set[str],
            transitions: t.Dict[str, t.Dict[str, t.Set[str]]],
            start_state: str,
            accepting_states: t.Set[str]
    ):
        """
        Constructor of NFA.

        Args:
            states (Set[str]): Set of states.
            alphabet (Set[str]): Alphabet.
            transitions (Dict[str, Dict[str, Set[str]]]): Transitions.
            start_state (str): Start state.
            accepting_states (Set[str]): Set of accepting states.
        """

        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def epsilon_closure(self, states: t.Union[t.Set, str]) -> t.Set[str]:
        """
        Compute the epsilon closure of a set of states.

        Args:
            states (Union[Set[str], str]): Set of states.

        Returns:
            Set[str]: Epsilon closure of the set of states.
        """

        closure = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            if current_state in self.transitions and '' in self.transitions[current_state]:
                new_states = self.transitions[current_state]['']
                for state in new_states:
                    if state not in closure:
                        closure.add(state)
                        stack.append(state)
        return closure

    def move(self, states: t.Union[t.Set[str], str], symbol: str) -> t.Set[str]:
        """
        Compute the set of states that can be reached from a set of states with a given symbol.

        Args:
            states (Union[Set[str], str]): Set of states.
            symbol (str): Symbol.

        Returns:
            Set[str]: Set of states that can be reached from the set of states with the given symbol.
        """

        result = set()
        for state in states:
            if state in self.transitions and symbol in self.transitions[state]:
                result.update(self.transitions[state][symbol])
        return result


class DFA:
    def __init__(
            self,
            states: t.Set[t.FrozenSet[str]],
            alphabet: t.Set[str],
            transitions: t.Dict[t.FrozenSet[str], t.Dict[str, t.FrozenSet[str]]],
            start_state: t.FrozenSet[str],
            accepting_states: t.Set[t.FrozenSet[str]]
    ):
        """
        Constructor of DFA.

        Args:
            states (Set[FrozenSet[str]]): Set of states.
            alphabet (Set[str]): Alphabet.
            transitions (Dict[FrozenSet[str], Dict[str, FrozenSet[str]]]): Transitions.
            start_state (FrozenSet[str]): Start state.
            accepting_states (Set[FrozenSet[str]]): Set of accepting states.
        """

        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def simulate(self, input_string: str) -> bool:
        """
        Simulate the DFA on a given input string.

        Args:
            input_string (str): Input string.

        Returns:
            bool: True if the DFA accepts the input string, False otherwise.
        """

        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet and symbol != '':
                raise NotInAlphabetError(symbol, self.alphabet)
            current_state = self.transitions[current_state][symbol]
        return current_state in self.accepting_states


def convert_nfa_to_dfa(nfa: NFA, print_process: bool = False) -> DFA:
    """
    Convert a NFA to a DFA.

    Args:
        nfa (NFA): NFA to convert.
        print_process (bool): Whether to print the conversion process.

    Returns:
        DFA: Converted DFA.
    """

    def print_process_if_needed(*args, **kwargs):
        if print_process:
            typing_effect(*args, **kwargs)

    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = frozenset(nfa.epsilon_closure({nfa.start_state}))
    dfa_accepting_states = set()

    print_process_if_needed("Start state of DFA is epsilon closure of start state of NFA:")
    print_process_if_needed(f"States: {dfa_states}")
    print_process_if_needed(f"Transitions: {dfa_transitions}")
    print_process_if_needed(f"Start States: {dfa_start_state}")
    print_process_if_needed(f"Accepting states: {dfa_accepting_states}")

    # Queue for states to process
    states_to_process = [dfa_start_state]
    print_process_if_needed(f"Queue: {states_to_process}")

    while states_to_process:
        current_dfa_state = states_to_process.pop()
        print_process_if_needed(f"Processing state: {current_dfa_state}")

        if current_dfa_state not in dfa_states:
            print_process_if_needed(f"State {current_dfa_state} is not in DFA states, adding it...")
            dfa_states.add(current_dfa_state)

        for symbol in nfa.alphabet:
            print_process_if_needed(f"Processing symbol: {symbol}")
            next_nfa_states = set()
            for nfa_state in current_dfa_state:
                print_process_if_needed(f"Processing NFA state: {nfa_state}")
                next_nfa_states.update(nfa.epsilon_closure(nfa.move({nfa_state}, symbol)))

            next_dfa_state = frozenset(next_nfa_states)
            print_process_if_needed(f"Next DFA state: {next_dfa_state}")

            if next_dfa_state not in dfa_states:
                print_process_if_needed(f"State {next_dfa_state} is not in DFA states, adding it...")
                states_to_process.append(next_dfa_state)

            if current_dfa_state not in dfa_transitions:
                print_process_if_needed(f"State {current_dfa_state} is not in DFA transitions, adding it...")
                dfa_transitions[current_dfa_state] = {}
            dfa_transitions[current_dfa_state][symbol] = next_dfa_state
            print_process_if_needed(f"Transitions: {dfa_transitions}")

    for dfa_state in dfa_states:
        print_process_if_needed(f"Processing DFA state: {dfa_state}")
        if any(nfa_state in nfa.accepting_states for nfa_state in dfa_state):
            print_process_if_needed(
                f"State {dfa_state} contains an accepting state of NFA, adding it to DFA accepting states...")
            dfa_accepting_states.add(dfa_state)

    print_process_if_needed(f"Final DFA states: {dfa_states}")

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accepting_states)


def main():
    # Define NFA
    nfa_states = {'q0', 'q1', 'q2'}
    nfa_alphabet = {'0', '1'}
    nfa_transitions = {
        'q0': {
            '': {'q1'}
        },
        'q1': {
            '0': {'q2'},
            '1': {'q1'}
        },
        'q2': {
            '0': {'q2'},
            '1': {'q2'}
        }
    }
    nfa_start_state = 'q0'
    nfa_accepting_states = {'q2'}

    nfa = NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_start_state, nfa_accepting_states)

    # print out the NFA with explanation
    typing_effect("Our NFA is defined as follows:")
    typing_effect(f"States: {nfa.states}")
    typing_effect(f"Alphabet: {nfa.alphabet}")

    # print out the NFA transitions in human readable format:
    typing_effect("Transitions:")
    for state in nfa.transitions:
        for symbol in nfa.transitions[state]:
            for next_state in nfa.transitions[state][symbol]:
                typing_effect(f"({state}, {symbol}) -> {next_state}")

    typing_effect(f"Start state: {nfa.start_state}")
    typing_effect(f"Accepting states: {nfa.accepting_states}")

    typing_effect("*" * 50, char_speed=0.01, space_speed=0.01)

    typing_effect("Do you want to print the conversion process? (y/n)")
    print_process = input().lower() == 'y'

    # Convert NFA to DFA
    dfa = convert_nfa_to_dfa(nfa, print_process=print_process)

    # Example 1: Accepting case
    input_string_accept = '0111'
    typing_effect(f"Example Input: {input_string_accept}")
    typing_effect("Converting NFA to DFA...")
    time.sleep(1)
    result_accept = dfa.simulate(input_string_accept)
    typing_effect(f"Input: {input_string_accept}, is {"accepted" if result_accept else "rejected"}")

    typing_effect("*" * 50, char_speed=0.01, space_speed=0.01)

    # Example 2: Rejecting case
    input_string_reject = '1'
    typing_effect(f"Example Input: {input_string_reject}")
    typing_effect("Converting NFA to DFA...")
    result_reject = dfa.simulate(input_string_reject)
    typing_effect(f"Input: {input_string_reject}, is {"accepted" if result_reject else "rejected"}")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
