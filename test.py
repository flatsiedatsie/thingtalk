from action import Action
from event import Event
from property import Property
from thing import Thing

from value import Value
from containers import SingleThing

# import logging
import time
import uuid


class OverheatedEvent(Event):
    def __init__(self, thing, data):
        Event.__init__(self, thing, "overheated", data=data)


class FadeAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "fade", input_=input_)

    async def perform_action(self):
        time.sleep(self.input["duration"] / 1000)
        await self.thing.set_property("brightness", self.input["brightness"])
        await self.thing.add_event(OverheatedEvent(self.thing, 102))


async def make_thing():
    thing = Thing(
        "urn:dev:ops:my-lamp-1234",
        "My Lamp",
        ["OnOffSwitch", "Light"],
        "A web connected lamp",
    )

    await thing.add_property(
        Property(
            thing,
            "on",
            Value(True),
            metadata={
                "@type": "OnOffProperty",
                "title": "On/Off",
                "type": "boolean",
                "description": "Whether the lamp is turned on",
            },
        )
    )
    await thing.add_property(
        Property(
            thing,
            "brightness",
            Value(50),
            metadata={
                "@type": "BrightnessProperty",
                "title": "Brightness",
                "type": "integer",
                "description": "The level of light from 0-100",
                "minimum": 0,
                "maximum": 100,
                "unit": "percent",
            },
        )
    )

    await thing.add_available_action(
        "fade",
        {
            "title": "Fade",
            "description": "Fade the lamp to a given level",
            "input": {
                "type": "object",
                "required": ["brightness", "duration",],
                "properties": {
                    "brightness": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100,
                        "unit": "percent",
                    },
                    "duration": {
                        "type": "integer",
                        "minimum": 1,
                        "unit": "milliseconds",
                    },
                },
            },
        },
        FadeAction,
    )

    await thing.add_available_event(
        "overheated",
        {
            "description": "The lamp has exceeded its safe operating temperature",
            "type": "number",
            "unit": "degree celsius",
        },
    )
    return SingleThing(thing)
