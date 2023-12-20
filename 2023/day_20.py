from utils import get_input, get_test_input, run


class Dummy:
    def __init__(self, name):
        self.name = name
        self.receivers = []
        self.pulses = [0, 0]

    def __repr__(self):
        return f"Dummy({self.name})"


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.receivers = []
        self.state = False  # off = False, on = True
        self.pulses = [0, 0]
        self.has_to_broadcast = False

    def __repr__(self):
        return f"FlipFlop({self.name})"


class Button:
    def __init__(self):
        self.name = "button"
        self.receivers = []
        self.pulses = [0, 0]


class Broadcaster:
    def __init__(self):
        self.name = "broadcaster"
        self.receivers = []
        self.pulses = [0, 0]

    def __repr__(self):
        return f"Broadcaster()"


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.receivers = []
        self.pulses = [0, 0]
        self.inputs = {}

    def __repr__(self):
        return f"Conjunction({self.name})"


def parse_input(input):
    lines = input.splitlines()
    receivers_map = {}
    modules = {}
    for line in lines:
        labeled_name, receivers_str = line.split(" -> ")
        receivers = receivers_str.split(", ")
        if labeled_name == "broadcaster":
            modules["broadcaster"] = Broadcaster()
            receivers_map["broadcaster"] = receivers
        else:
            label = labeled_name[:1]
            name = labeled_name[1:]
            receivers_map[name] = receivers
            if label == "%":
                modules[name] = FlipFlop(name)
            elif label == "&":
                modules[name] = Conjunction(name)
            else:
                raise Exception(f"Unknown module type: {label}")

    for name, receivers in receivers_map.items():
        for r in receivers:
            if r not in modules:
                modules[r] = Dummy(r)
            modules[name].receivers.append(modules[r])

    button_module = Button()
    button_module.receivers = [modules["broadcaster"]]
    modules["button"] = button_module

    # identify Conjunction inputs
    for name, module in modules.items():
        for receiver in module.receivers:
            if isinstance(receiver, Conjunction):
                receiver.inputs[name] = False

    return modules


def process_pulse(modules, name, pulse, sender):
    module = modules[name]
    if isinstance(module, Button):
        return module
    elif isinstance(module, Broadcaster):
        return module
    elif isinstance(module, FlipFlop):
        if not pulse:
            module.state = not module.state
            module.has_to_broadcast = True
            return module
    elif isinstance(module, Conjunction):
        module.inputs[sender.name] = pulse
        return module


def broadcast_pulse(modules, names):
    modules_to_broadcast = []
    for name in names:
        module = modules[name]
        if isinstance(module, Button):
            for receiver in module.receivers:
                module.pulses[False] += 1
                modules_to_broadcast.append(
                    process_pulse(modules, receiver.name, False, module)
                )
        elif isinstance(module, Broadcaster):
            for receiver in module.receivers:
                module.pulses[False] += 1
                modules_to_broadcast.append(
                    process_pulse(modules, receiver.name, False, module)
                )

        elif isinstance(module, FlipFlop):
            if module.has_to_broadcast:
                module.has_to_broadcast = False
                for receiver in module.receivers:
                    module.pulses[module.state] += 1
                    modules_to_broadcast.append(
                        process_pulse(modules, receiver.name, module.state, module)
                    )

        elif isinstance(module, Conjunction):
            is_all_high_pulse = all(module.inputs.values())
            for receiver in module.receivers:
                module.pulses[not is_all_high_pulse] += 1
                modules_to_broadcast.append(
                    process_pulse(modules, receiver.name, not is_all_high_pulse, module)
                )

    return [x for x in modules_to_broadcast if x]


def count_pulses(modules):
    for _ in range(1000):
        modules_to_broadcast = broadcast_pulse(modules, ["button"])
        while modules_to_broadcast:
            modules_to_broadcast = broadcast_pulse(
                modules, [m.name for m in modules_to_broadcast]
            )

    n_low_pulses = sum([m.pulses[False] for m in modules.values()])
    n_high_pulses = sum([m.pulses[True] for m in modules.values()])
    return n_low_pulses * n_high_pulses


def test1(input, expected):
    modules = parse_input(input)
    assert count_pulses(modules) == expected


def test():
    test1(get_test_input(__file__), 32000000)
    test1(get_test_input(__file__, "2"), 11687500)


def main():
    input = get_input(__file__)
    modules = parse_input(input)
    print("Part 1:", count_pulses(modules))


run(main, test, ignore_other_exceptions=False)
