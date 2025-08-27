import unittest
from solidity_audit_lib.messaging import SignedMessage, TimestampedMessage
from bittensor import Keypair as BTKeypair
from hypothesis import given, strategies as st
import time


class TestMessagingCryptoPart(unittest.TestCase):

    def setUp(self):
        self.keypair = BTKeypair.create_from_mnemonic(BTKeypair.generate_mnemonic())

    def test_sign_and_verify(self):
        message = SignedMessage(content="Hello, world!")
        message.sign(self.keypair)
        self.assertTrue(message.verify())

    def test_verify_without_signature(self):
        message = SignedMessage(content="Hello, world!")
        self.assertFalse(message.verify())

    def test_verify_with_invalid_signature(self):
        message = SignedMessage(content="Hello, world!")
        message.sign(self.keypair)
        message.ss58_address = BTKeypair.create_from_mnemonic(
            BTKeypair.generate_mnemonic()
        ).ss58_address

        self.assertFalse(message.verify())

    @given(st.text())
    def test_sign_and_verify_with_hypothesis(self, content):
        message = SignedMessage(content=content)
        message.sign(self.keypair)
        self.assertTrue(message.verify())

    def test_sign_and_verify_with_extra_fields(self):
        message = SignedMessage(content="Extra fields", extra_field=123)
        message.sign(self.keypair)
        self.assertTrue(message.verify())

    def test_timestamped_message_sign_sets_timestamp(self):
        msg = TimestampedMessage(content="Test timestamp")
        self.assertIsNone(msg.timestamp)
        msg.sign(self.keypair)
        self.assertIsNotNone(msg.timestamp)
        self.assertTrue(abs(msg.timestamp - int(time.time())) < 5)
        self.assertTrue(msg.verify())

    def test_verify_raises_on_invalid_signature_when_safe_false(self):
        msg = SignedMessage(content="Test")
        msg.sign(self.keypair)
        msg.signature = "0xdeadbeef"
        with self.assertRaises(Exception):
            msg.verify(safe=False)

    @given(st.text())
    def test_signature_should_always_work_with_hypothesis(self, content):
        initial_msg = TimestampedMessage(content=content)
        initial_msg.sign(self.keypair)
        self.assertIsNotNone(initial_msg.signature)
        self.assertIsNotNone(initial_msg.ss58_address)

        # Serialize and deserialize the message
        # to ensure the signature and address are preserved
        # This simulates the real-world usage where messages are often serialized
        # before being sent over a network or stored.
        serialized_msg = initial_msg.model_dump()
        deser_message = SignedMessage(**serialized_msg)
        self.assertTrue(deser_message.verify())


if __name__ == "__main__":
    unittest.main()
