<?php declare(strict_types = 1);

namespace Adshares\AdPay\Tests\Application\DTO;

use Adshares\AdPay\Application\DTO\CampaignDeleteDTO;
use Adshares\AdPay\Application\Exception\ValidationException;
use PHPUnit\Framework\TestCase;

final class CampaignDeleteDTOTest extends TestCase
{
    public function testEmptyInputData(): void
    {
        $this->expectException(ValidationException::class);

        new CampaignDeleteDTO([]);
    }

    /**
     * @dataProvider validIdDataProvider
     */
    public function testValidIdData(array $data, int $count = 1): void
    {
        $dto = new CampaignDeleteDTO(['campaigns' => $data]);

        $this->assertCount($count, $dto->getIds());
    }

    /**
     * @dataProvider invalidIdDataProvider
     */
    public function testInvalidIdData(array $data): void
    {
        $this->expectException(ValidationException::class);

        new CampaignDeleteDTO(['campaigns' => $data]);
    }

    public function validIdDataProvider(): array
    {
        return [
            [[], 0],
            [['43c567e1396b4cadb52223a51796fd01']],
            [['ffc567e1396b4cadb52223a51796fdff', '43c567e1396b4cadb52223a51796fd01'], 2],
            [
                [
                    'ffc567e1396b4cadb52223a51796fdff',
                    '43c567e1396b4cadb52223a51796fd01',
                    'ffc567e1396b4cadb52223a51796fdff',
                ],
                3,
            ],
        ];
    }

    public function invalidIdDataProvider(): array
    {
        return [
            [[123]],
            [['invalid']],
            [['ffc567e1396b4cadb52223a51796fdff', 'xyz']],
        ];
    }
}