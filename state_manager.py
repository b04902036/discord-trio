from state import State, StateBase, StatePersistence
from states.getting_user_count import GettingUserCountState
from states.registering_user import RegisteringUserState
from states.game_running import GameRunningState

# StateManager to handle transitions
class StateManager:
    def __init__(self):
        self.state = State.GETTING_USER_COUNT
        self.state_classes = {
            State.GETTING_USER_COUNT: GettingUserCountState,
            State.REGISTERING_USER: RegisteringUserState,
            State.GAME_RUNNING: GameRunningState,
        }

        self.persistence = StatePersistence(self.state, 0, [], None)
        self.state_obj = self.state_classes[self.state](self.persistence)

    async def banner(self):
        return await self.state_obj.banner()

    async def process_input(self, msg):
        """Processes input based on the current state and moves to the next state."""
        current_state_obj: StateBase = self.state_obj
        try:
            next_state = await current_state_obj.input(msg)
        except Exception as e:
            print(f"failed to process input {msg}, error: {e}")
            return
        if next_state != self.state:
            self.state = next_state
            self.persistence = current_state_obj.persistence
            self.persistence.state = next_state
            self.state_obj = self.state_classes[self.state](self.persistence)
            await self.state_obj.init()
        