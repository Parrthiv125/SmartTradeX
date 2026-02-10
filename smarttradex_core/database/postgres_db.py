import psycopg2
from datetime import datetime


class PostgresDB:
    def __init__(self):
        """
        Supabase PostgreSQL connection
        Replace credentials with your actual project values.
        """

        self.conn = psycopg2.connect(
            "postgresql://postgres:SmartTradeX125@db.chfnqgbcdcmeqnwfiwyn.supabase.co:5432/postgres"
        )

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    # --------------------------------------------------
    # INSERT NEW TRADE
    # --------------------------------------------------
    def insert_trade(
        self,
        entry_time,
        side,
        entry_price,
        quantity,
        confidence,
        strategy
    ):
        """
        Insert new OPEN trade into paper_trades table
        """

        query = """
        INSERT INTO paper_trades (
            entry_time,
            side,
            entry_price,
            quantity,
            confidence,
            strategy,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, 'OPEN');
        """

        self.cursor.execute(
            query,
            (
                entry_time,
                side,
                entry_price,
                quantity,
                confidence,
                strategy
            )
        )

    # --------------------------------------------------
    # CLOSE TRADE
    # --------------------------------------------------
    def close_trade(
        self,
        trade_id,
        exit_time,
        exit_price,
        pnl_pct,
        pnl_value
    ):
        """
        Close an OPEN trade and update PnL
        """

        query = """
        UPDATE paper_trades
        SET
            exit_time = %s,
            exit_price = %s,
            pnl_pct = %s,
            pnl_value = %s,
            status = 'CLOSED'
        WHERE trade_id = %s;
        """

        self.cursor.execute(
            query,
            (
                exit_time,
                exit_price,
                pnl_pct,
                pnl_value,
                trade_id
            )
        )

    # --------------------------------------------------
    # GET LAST OPEN TRADE
    # --------------------------------------------------
    def get_last_open_trade(self):
        """
        Fetch last OPEN trade_id
        """

        query = """
        SELECT trade_id
        FROM paper_trades
        WHERE status = 'OPEN'
        ORDER BY trade_id DESC
        LIMIT 1;
        """

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result:
            return result[0]
        return None

    # --------------------------------------------------
    # FETCH ALL TRADES
    # --------------------------------------------------
    def fetch_all_trades(self):
        """
        Return all stored trades
        """

        query = "SELECT * FROM paper_trades ORDER BY trade_id DESC;"
        self.cursor.execute(query)

        return self.cursor.fetchall()

    # --------------------------------------------------
    # CONNECTION TEST
    # --------------------------------------------------
    def test_connection(self):
        """
        Simple DB connectivity test
        """

        self.cursor.execute("SELECT NOW();")
        return self.cursor.fetchone()

    # --------------------------------------------------
    # STORE PREDICTION RESULT
    # --------------------------------------------------
    def insert_prediction(
        self,
        predicted_return,
        actual_return
    ):

        predicted_direction = (
            1 if predicted_return > 0 else -1
        )

        actual_direction = (
            1 if actual_return > 0 else -1
        )

        is_correct = (
            predicted_direction == actual_direction
        )

        query = """
        INSERT INTO model_predictions (
            timestamp,
            predicted_return,
            actual_return,
            predicted_direction,
            actual_direction,
            is_correct
        )
        VALUES (NOW(), %s, %s, %s, %s, %s);
        """

        self.cursor.execute(
            query,
            (
                predicted_return,
                actual_return,
                predicted_direction,
                actual_direction,
                is_correct
            )
        )
