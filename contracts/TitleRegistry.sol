// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";



contract TitleRegistry is Initializable, ERC721Upgradeable, ERC721EnumerableUpgradeable, ERC721URIStorageUpgradeable, OwnableUpgradeable, UUPSUpgradeable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    constructor() {
        _disableInitializers();
    }

    struct Title {
        string propertyOwner;
        string Jurisdiction;
        uint256 saleValue;
        string titleJson;
    }

    mapping(uint256 => Title) public savedTitles;

    event Sale(uint256 tokenId, uint256 saleValue, string reportURI, string titleJson);
    
    function initialize(address initialOwner) initializer public {
        __ERC721_init("Title Registry Token", "TIT");
        __ERC721Enumerable_init();
        __ERC721URIStorage_init();
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyOwner
        override
    {}

    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return savedTitles[tokenId].titleJson;
    }


    function registerTitle(
        address owner,
        string memory name,
        string memory Jurisdiction,
        uint256 initialSaleValue,
        string memory titleURI,
        string memory tokenJSON
    ) public returns (uint256) {
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        _mint(owner, newItemId);
        _setTokenURI(newItemId, titleURI);

        savedTitles[newItemId] = Title(name, Jurisdiction, initialSaleValue, tokenJSON);

        return newItemId;
    }

    function totalSupply () public view override returns (uint256) {
        return _tokenIds.current();
    }
    
    

    function newSale(
        uint256 tokenId,
        uint256 newSaleValue,
        string memory reportURI,
        string memory tokenJSON
        
    ) public returns (uint256) {
        savedTitles[tokenId].saleValue = newSaleValue;

        emit Sale(tokenId, newSaleValue, reportURI, tokenJSON);

        return (savedTitles[tokenId].saleValue);
    }


    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721Upgradeable, ERC721EnumerableUpgradeable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

     function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721Upgradeable, ERC721EnumerableUpgradeable)
    {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721Upgradeable, ERC721URIStorageUpgradeable)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Upgradeable, ERC721EnumerableUpgradeable, ERC721URIStorageUpgradeable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
