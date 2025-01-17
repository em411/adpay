<?php

declare(strict_types=1);

namespace Adshares\AdPay\Tests\Domain\Model;

use Adshares\AdPay\Domain\Model\Payment;
use Adshares\AdPay\Domain\Model\PaymentCollection;
use Adshares\AdPay\Domain\ValueObject\EventType;
use Adshares\AdPay\Domain\ValueObject\Id;
use Adshares\AdPay\Domain\ValueObject\PaymentStatus;
use PHPUnit\Framework\TestCase;

final class PaymentCollectionTest extends TestCase
{
    public function testMultiplyAdding(): void
    {
        $item1 = self::createPayment(1);
        $item2 = self::createPayment(2);
        $item3 = self::createPayment(3);
        $item4 = self::createPayment(4);

        $this->assertCount(4, new PaymentCollection($item1, $item2, $item3, $item4));
    }

    public function testEmptyCollection(): void
    {
        $collection = new PaymentCollection();

        $this->assertCount(0, $collection);
        $this->assertEmpty($collection);
    }

    private static function createPayment(int $id): Payment
    {
        return new Payment(
            EventType::createView(),
            new Id('43c567e1396b4cadb52223a51796fd0' . $id),
            new PaymentStatus(PaymentStatus::ACCEPTED)
        );
    }
}
