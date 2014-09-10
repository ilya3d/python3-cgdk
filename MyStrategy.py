from math import *
from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.HockeyistState import HockeyistState
from model.HockeyistType import HockeyistType
from model.World import World


class MyStrategy:
    STRIKE_ANGLE = pi / 180

    # me = None
    # world = None
    # game = None
    # me_move = None

    # noinspection PyMethodMayBeStatic
    def move(self, me: Hockeyist, world: World, game: Game, move: Move):

        # self.me = me
        # self.world = world
        # self.game = game
        # self.me_move = move

        if me.state == HockeyistState.SWINGING:
            move.action = ActionType.STRIKE
            return

        if world.puck.owner_player_id == me.player_id:

            if world.puck.owner_hockeyist_id == me.id:

                opponent = world.get_opponent_player()

                net_x = 0.5 * (opponent.net_back + opponent.net_front)
                net_y = 0.5 * (opponent.net_bottom + opponent.net_top)

                angle_to_net = me.get_angle_to(net_x, net_y)
                move.turn = angle_to_net

                if abs(angle_to_net) < self.STRIKE_ANGLE:
                    move.action = ActionType.STRIKE

            else:

                nearest_opponent = self.get_nearest_opponent(me, world)

                if nearest_opponent is not None:

                    if me.get_distance_to_unit(nearest_opponent) > game.stick_length:
                        move.speed_up = 1
                    else:
                        move.action = ActionType.STRIKE

                    move.turn = me.get_angle_to_unit(nearest_opponent)

        else:
            move.speed_up = 1
            move.turn = me.get_angle_to_unit(world.puck)
            move.action = ActionType.TAKE_PUCK

    @staticmethod
    def get_nearest_opponent(me: Hockeyist, world: World):

        """
        Отдает ближайшего хоккеиста противника
        :param me: Hockeyist
        :param world: World
        :return: Hockeyist
        """
        nearest_opponent = None
        nearest_opponent_range = 0

        for hockeyist in world.hockeyists:

            if hockeyist.teammate \
                    or hockeyist.type == HockeyistType.GOALIE \
                    or hockeyist.state == HockeyistState.KNOCKED_DOWN \
                    or hockeyist.state == HockeyistState.KNOCKED_DOWN \
                    or hockeyist.state == HockeyistState.RESTING:
                continue

            opponent_range = me.get_distance_to_unit(hockeyist)

            if nearest_opponent is None or opponent_range < nearest_opponent_range:
                nearest_opponent = hockeyist
                nearest_opponent_range = opponent_range

        return nearest_opponent
