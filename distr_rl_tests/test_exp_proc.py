from ssbm_bot.distr_rl import trainer

if __name__ == '__main__':
    trainer.process_exps_loop(
        exp_port=50000,
        return_port=50002,
        window_size=15,
        frame_delay=5,
        exp_batch_size=16
    )