<?php

declare(strict_types=1);

namespace Adshares\AdPay\Application\DTO;

use Adshares\AdPay\Domain\Model\ClickEvent;
use Adshares\AdPay\Domain\Model\Event;
use Adshares\AdPay\Domain\Model\EventCollection;
use Adshares\AdPay\Domain\ValueObject\EventType;
use Adshares\AdPay\Domain\ValueObject\Id;
use Adshares\AdPay\Lib\DateTimeHelper;
use DateTimeInterface;

final class ClickEventUpdateDTO extends EventUpdateDTO
{
    protected function createEventCollection(DateTimeInterface $timeStart, DateTimeInterface $timeEnd): EventCollection
    {
        return new EventCollection(EventType::createClick(), $timeStart, $timeEnd);
    }

    protected function createEventModel(array $input): Event
    {
        return new ClickEvent(
            new Id($input['id']),
            DateTimeHelper::fromTimestamp($input['time']),
            $this->createImpressionCaseModel($input)
        );
    }
}
