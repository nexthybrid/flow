import logging

from cistar.core.exp import SumoExperiment
from cistar.envs.loop_velocity import SimpleVelocityEnvironment
from cistar.scenarios.loop.loop_scenario import LoopScenario
from cistar.controllers.velocity_controllers import *

logging.basicConfig(level=logging.INFO)

tot_cars = 12

auton_cars = 2
human_cars = tot_cars - auton_cars

sumo_params = {"port": 8873, "time_step":0.1}

sumo_binary = "sumo"

# type_params = {"bcm-15": (10, make_better_cfm(v_des = 15, k_c=2.0)), "bcm-10": (7, make_better_cfm(v_des = 10, k_c=2.0))}
type_params = {"rl":(auton_cars, None), "bcm-15": (human_cars, make_better_cfm(v_des = 15, k_c = 2.0))}

env_params = {"target_velocity": 25}

net_params = {"length": 200, "lanes": 1, "speed_limit":35, "resolution": 40, "net_path":"debug/net/"}

cfg_params = {"start_time": 0, "end_time":3000, "cfg_path":"leah/cfg/"}

initial_positions = [("top", 0), ("top", 70), ("top", 140), \
                    ("left", 0), ("left", 70), ("left", 140), \
                    ("bottom", 0), ("bottom", 70), ("bottom", 140), \
                    ("right", 0), ("right", 70), ("right", 140)]
initial_config = {"positions": initial_positions, "shuffle": False}

scenario = LoopScenario("test-exp", tot_cars, type_params, cfg_params, net_params, initial_config=initial_config, generator_class=CircleGenerator)

exp = SumoExperiment(SimpleVelocityEnvironment, env_params, sumo_binary, sumo_params, scenario)

logging.info("Experiment Set Up complete")

print("experiment initialized")

env = normalize(exp.env)

for seed in [1]: # [1, 5, 10, 73, 56]
    policy = GaussianMLPPolicy(
        env_spec=env.spec,
        hidden_sizes=(32,32)
    )

    baseline = LinearFeatureBaseline(env_spec=env.spec)

    algo = TRPO(
        env=env,
        policy=policy,
        baseline=baseline,
        batch_size=2000,
        max_path_length=400,
        # whole_paths=True,
        n_itr=1500,
        # discount=0.99,
        # step_size=0.01,
    )
    # algo.train()

    run_experiment_lite(
        algo.train(),
        # Number of parallel workers for sampling
        n_parallel=1,
        # Only keep the snapshot parameters for the last iteration
        snapshot_mode="last",
        # Specifies the seed for the experiment. If this is not provided, a random seed
        # will be used
        seed=seed,
        mode="local",
        exp_prefix="leah-test-exp"
        # plot=True,
    )

exp.env.terminate()